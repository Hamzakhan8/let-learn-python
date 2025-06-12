# -*- coding: utf-8 -*-
"""
Futuristic AI-Powered Student Learning Assistant
A cutting-edge educational platform with AI integration
"""

import os
import re
import json
import random
import requests
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import wikipedia
import urllib.parse

# Create Flask application with SocketIO
app = Flask(__name__)
app.secret_key = 'futuristic-ai-learning-assistant-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Add custom Jinja2 filter for JSON conversion
@app.template_filter('tojsonfilter')
def to_json_filter(obj):
    return json.dumps(obj)

# Ollama AI Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"

def check_ollama_connection():
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False

def get_ai_recommendation(query, user_profile=None):
    """Get AI-powered course recommendations"""
    try:
        if not check_ollama_connection():
            return get_fallback_recommendation(query)
        
        prompt = f"""As an expert educational AI, provide personalized learning recommendations for: "{query}"

Please respond with a JSON object containing:
- recommendation: Brief personalized advice
- course_structure: Array of 4-5 main learning topics
- difficulty: Difficulty level
- time_estimate: Estimated learning time
- prerequisites: What they should know first
- fun_facts: Interesting motivation about the topic

Keep it encouraging and practical."""
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            return parse_ai_response(result.get('response', ''))
        else:
            return get_fallback_recommendation(query)
            
    except Exception as e:
        print(f"AI error: {e}")
        return get_fallback_recommendation(query)

def parse_ai_response(response_text):
    """Parse AI response into structured data"""
    try:
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    return {
        "recommendation": "Excellent choice! This is a valuable subject that will expand your knowledge and skills.",
        "course_structure": ["Introduction & Basics", "Core Concepts", "Practical Applications", "Advanced Topics", "Real-world Projects"],
        "difficulty": "Beginner to Intermediate",
        "time_estimate": "3-6 weeks",
        "prerequisites": "Basic curiosity and dedication",
        "fun_facts": "This field has amazing applications in many industries!"
    }

def get_fallback_recommendation(query):
    """Fallback when AI is unavailable"""
    return {
        "recommendation": f"Great choice! {query.title()} is an excellent subject to learn with many practical applications.",
        "course_structure": ["Fundamentals", "Core Concepts", "Practice & Examples", "Advanced Topics", "Real Projects"],
        "difficulty": "All Levels",
        "time_estimate": "2-8 weeks",
        "prerequisites": "Enthusiasm to learn!",
        "fun_facts": f"{query.title()} opens doors to exciting career opportunities!"
    }

# Database Setup
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            email TEXT,
            level INTEGER DEFAULT 1,
            total_points INTEGER DEFAULT 0,
            learning_streak INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            topic TEXT,
            progress_percentage REAL DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_database()

# Enhanced categories with courses
SUBJECT_CATEGORIES = {
    'mathematics': {
        'name': 'Mathematics',
        'icon': 'fa-calculator',
        'keywords': ['math', 'algebra', 'geometry', 'calculus', 'statistics'],
        'color': '#10b981',
        'courses': [
            {
                'id': 'basic-math',
                'title': 'Mathematics Fundamentals',
                'description': 'Master the basics of mathematics with step-by-step guidance',
                'duration': '4 weeks',
                'level': 'Beginner',
                'rating': 4.9,
                'students': 12500,
                'modules': ['Numbers & Operations', 'Basic Algebra', 'Geometry Basics', 'Problem Solving', 'Applications']
            }
        ]
    },
    'programming': {
        'name': 'Programming',
        'icon': 'fa-code',
        'keywords': ['python', 'javascript', 'coding', 'programming', 'software'],
        'color': '#8b5cf6',
        'courses': [
            {
                'id': 'python-basics',
                'title': 'Python Programming Mastery',
                'description': 'Learn Python from scratch to advanced level',
                'duration': '6 weeks',
                'level': 'Beginner',
                'rating': 4.9,
                'students': 25600,
                'modules': ['Python Basics', 'Data Types', 'Control Flow', 'Functions', 'OOP', 'Projects']
            }
        ]
    },
    'science': {
        'name': 'Science',
        'icon': 'fa-atom',
        'keywords': ['physics', 'chemistry', 'biology', 'science'],
        'color': '#06b6d4',
        'courses': [
            {
                'id': 'physics-101',
                'title': 'Physics Fundamentals',
                'description': 'Explore the laws of nature and physics',
                'duration': '8 weeks',
                'level': 'Beginner',
                'rating': 4.8,
                'students': 15200,
                'modules': ['Mechanics', 'Thermodynamics', 'Waves', 'Electricity', 'Modern Physics']
            }
        ]
    }
}

# Utility functions
def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(10000, 99999)}"
    return session['user_id']

def log_search(query, user_id):
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search_analytics (user_id, query) VALUES (?, ?)", (user_id, query))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Search logging error: {e}")

def get_trending_topics():
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT query, COUNT(*) as count 
            FROM search_analytics 
            WHERE timestamp > datetime('now', '-7 days')
            GROUP BY query 
            ORDER BY count DESC 
            LIMIT 8
        """)
        results = cursor.fetchall()
        conn.close()
        return [topic[0] for topic in results] if results else ['Python Programming', 'Mathematics', 'Web Development', 'Data Science']
    except:
        return ['Python Programming', 'Mathematics', 'Web Development', 'Data Science', 'Machine Learning', 'Physics']

# Flask routes
@app.route('/')
def home():
    user_id = get_user_id()
    trending_topics = get_trending_topics()
    recent_searches = session.get('recent_searches', [])
    
    # Get user data from database
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, total_points, level) VALUES (?, 0, 1)
    ''', (user_id,))
    
    cursor.execute('SELECT total_points, level FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        total_points, level = result
        # Ensure level is calculated correctly
        calculated_level = max(1, total_points // 100 + 1)
        if calculated_level != level:
            cursor.execute('UPDATE users SET level = ? WHERE id = ?', (calculated_level, user_id))
            level = calculated_level
    else:
        total_points, level = 0, 1
    
    conn.commit()
    conn.close()
    
    user_data = {
        'points': total_points,
        'level': level,
        'search_count': len(recent_searches)
    }
    
    return render_template('index.html', 
                         categories=SUBJECT_CATEGORIES,
                         recent_searches=recent_searches,
                         trending_topics=trending_topics,
                         user_id=user_id,
                         user_data=user_data)

@app.route('/test')
def test_search():
    """Test page for search functionality"""
    with open('test_search.html', 'r', encoding='utf-8') as f:
        return f.read(), 200, {'Content-Type': 'text/html'}

@app.route('/api/search_suggestions/<query>')
def search_suggestions(query):
    """Real-time search suggestions"""
    suggestions = []
    query_lower = query.lower()
    
    for cat_key, cat_data in SUBJECT_CATEGORIES.items():
        if query_lower in cat_data['name'].lower():
            suggestions.append({
                'text': cat_data['name'],
                'type': 'category',
                'icon': cat_data['icon']
            })
        
        for keyword in cat_data['keywords']:
            if query_lower in keyword.lower() and len(suggestions) < 8:
                suggestions.append({
                    'text': keyword.title(),
                    'type': 'topic',
                    'icon': cat_data['icon']
                })
    
    return jsonify(suggestions[:8])

@app.route('/api/suggestions')
def get_suggestions():
    """Get search suggestions"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'suggestions': []})
    
    suggestions = []
    query_lower = query.lower()
    
    # Add category suggestions
    for cat_key, cat_data in SUBJECT_CATEGORIES.items():
        if query_lower in cat_data['name'].lower():
            suggestions.append(cat_data['name'])
        
        for keyword in cat_data['keywords']:
            if query_lower in keyword.lower() and keyword.title() not in suggestions:
                suggestions.append(keyword.title())
    
    # Add some common educational topics
    common_topics = [
        'How to learn effectively', 'Study techniques', 'Time management',
        'Note taking methods', 'Memory improvement', 'Critical thinking',
        'Problem solving', 'Research skills', 'Presentation skills'
    ]
    
    for topic in common_topics:
        if query_lower in topic.lower() and topic not in suggestions:
            suggestions.append(topic)
    
    return jsonify({'suggestions': suggestions[:8]})

@app.route('/api/track', methods=['POST'])
def track_activity():
    """Track user activities for points and analytics"""
    data = request.get_json()
    action = data.get('action', 'unknown')
    course_id = data.get('course_id', '')
    
    user_id = get_user_id()
    
    # Award points based on activity
    points_awarded = 0
    if action == 'course_view':
        points_awarded = 10
    elif action == 'search':
        points_awarded = 5
    elif action == 'chat_message':
        points_awarded = 2
    
    # Update user points in database
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, total_points) VALUES (?, 0)
    ''', (user_id,))
    
    cursor.execute('''
        UPDATE users SET total_points = total_points + ? WHERE id = ?
    ''', (points_awarded, user_id))
    
    # Get updated user data
    cursor.execute('SELECT total_points, level FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        total_points, level = result
        # Calculate level based on points (every 100 points = 1 level)
        new_level = max(1, total_points // 100 + 1)
        if new_level != level:
            cursor.execute('UPDATE users SET level = ? WHERE id = ?', (new_level, user_id))
            level = new_level
    else:
        total_points, level = points_awarded, 1
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'points_awarded': points_awarded,
        'user_data': {
            'points': total_points,
            'level': level,
            'search_count': len(session.get('recent_searches', []))
        }
    })

@app.route('/api/search', methods=['POST'])
def dynamic_search():
    """Enhanced search with AI recommendations and course popups"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    user_id = get_user_id()
    log_search(query, user_id)
    
    # Update recent searches
    if 'recent_searches' not in session:
        session['recent_searches'] = []
    if query not in session['recent_searches']:
        session['recent_searches'].insert(0, query)
        session['recent_searches'] = session['recent_searches'][:10]
    
    # Get AI recommendation
    ai_recommendation = get_ai_recommendation(query)
    
    # Find related courses
    related_courses = []
    for cat_key, cat_data in SUBJECT_CATEGORIES.items():
        if any(keyword in query.lower() for keyword in cat_data['keywords']) or query.lower() in cat_data['name'].lower():
            for course in cat_data.get('courses', []):
                related_courses.append({
                    'id': course['id'],
                    'title': course['title'],
                    'description': course['description'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'rating': course.get('rating', 4.5),
                    'students': course.get('students', 1000),
                    'modules': course['modules'][:4],
                    'category': cat_data['name'],
                    'color': cat_data['color'],
                    'icon': cat_data['icon']
                })
    
    # Generate dynamic learning path
    learning_path = [
        {"step": 1, "title": "Start with Basics", "description": f"Begin your {query} journey with fundamental concepts"},
        {"step": 2, "title": "Practice & Apply", "description": "Work on hands-on exercises and real examples"},
        {"step": 3, "title": "Build Projects", "description": "Create practical projects to solidify your learning"},
        {"step": 4, "title": "Advanced Topics", "description": "Explore advanced concepts and specializations"}
    ]
    
    # Award points for search
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, total_points) VALUES (?, 0)
    ''', (user_id,))
    
    cursor.execute('''
        UPDATE users SET total_points = total_points + 5 WHERE id = ?
    ''', (user_id,))
    
    # Get updated user data
    cursor.execute('SELECT total_points, level FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        total_points, level = result
        new_level = max(1, total_points // 100 + 1)
        if new_level != level:
            cursor.execute('UPDATE users SET level = ? WHERE id = ?', (new_level, user_id))
            level = new_level
    else:
        total_points, level = 5, 1
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'query': query,
        'courses': related_courses[:6],  # Template expects 'courses' not 'related_courses'
        'ai_recommendation': ai_recommendation,
        'learning_path': learning_path,
        'estimated_completion': ai_recommendation.get('time_estimate', '4-6 weeks'),
        'difficulty_match': True,
        'personalized': True,
        'user_data': {
            'points': total_points,
            'level': level,
            'search_count': len(session.get('recent_searches', []))
        }
    })

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    """Real-time AI chat"""
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        if check_ollama_connection():
            prompt = f"""You are a friendly AI tutor helping students learn. A student says: "{message}"

Provide a helpful, encouraging response in 2-3 sentences. Be conversational and supportive. If they ask about a topic, give practical learning advice."""
            
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '').strip()
            else:
                raise Exception("AI unavailable")
        else:
            raise Exception("Ollama not connected")
            
    except:
        ai_response = "I'm here to help you learn! That's a great question. Let me suggest exploring our courses and materials to find detailed information on this topic."
    
    return jsonify({
        'response': ai_response,
        'suggestions': [
            'Tell me more about this',
            'Show me examples',
            'What should I learn next?',
            'How can I practice this?'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/voice_search', methods=['POST'])
def voice_search():
    """Process voice search input"""
    data = request.get_json()
    transcript = data.get('transcript', '').strip()
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400
    
    # Process voice commands
    processed_query = transcript
    action = 'search'
    
    if 'search for' in transcript.lower():
        processed_query = transcript.lower().replace('search for', '').strip()
    elif 'learn about' in transcript.lower():
        processed_query = transcript.lower().replace('learn about', '').strip()
    elif 'show me' in transcript.lower():
        processed_query = transcript.lower().replace('show me', '').strip()
    elif 'help with' in transcript.lower():
        processed_query = transcript.lower().replace('help with', '').strip()
        action = 'help'
    
    return jsonify({
        'success': True,
        'original_transcript': transcript,
        'processed_query': processed_query.title(),
        'action': action,
        'confidence': 0.95
    })

@app.route('/api/toggle_theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark theme"""
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    
    return jsonify({
        'success': True,
        'theme': new_theme,
        'message': f'Switched to {new_theme} mode'
    })

@app.route('/api/award_points', methods=['POST'])
def award_points():
    """Award points for learning activities"""
    data = request.get_json()
    activity = data.get('activity', 'search')
    
    point_values = {
        'search': 5,
        'course_view': 10,
        'lesson_complete': 25,
        'quiz_complete': 20,
        'daily_login': 15,
        'streak_bonus': 50
    }
    
    points = point_values.get(activity, 5)
    current_points = session.get('user_points', 0)
    new_total = current_points + points
    session['user_points'] = new_total
    
    # Level up logic
    current_level = session.get('user_level', 1)
    new_level = (new_total // 100) + 1
    level_up = new_level > current_level
    if level_up:
        session['user_level'] = new_level
    
    return jsonify({
        'success': True,
        'points_awarded': points,
        'total_points': new_total,
        'level': new_level,
        'level_up': level_up,
        'next_level_points': (new_level * 100) - new_total
    })

# WebSocket events
@socketio.on('join_room')
def on_join(data):
    """Join study room for collaborative learning"""
    room = data.get('room', 'general')
    user_id = get_user_id()
    join_room(room)
    emit('user_joined', {
        'user_id': user_id,
        'message': f'Student {user_id} joined the study room',
        'timestamp': datetime.now().isoformat()
    }, room=room)

@socketio.on('send_message')
def on_message(data):
    """Send message in study room"""
    room = data.get('room', 'general')
    message = data.get('message', '')
    user_id = get_user_id()
    
    emit('receive_message', {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, room=room)

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle AI chat messages"""
    message = data.get('message', '').strip()
    user_id = get_user_id()
    
    if not message:
        return
    
    try:
        if check_ollama_connection():
            prompt = f"""You are a friendly AI tutor helping students learn. A student says: "{message}"

Provide a helpful, encouraging response in 2-3 sentences. Be conversational and supportive. If they ask about a topic, give practical learning advice."""
            
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '').strip()
            else:
                raise Exception("AI unavailable")
        else:
            raise Exception("Ollama not connected")
            
    except:
        # Smart fallback responses based on message content
        message_lower = message.lower()
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            ai_response = "Hello! I'm your AI tutor. I'm here to help you learn anything you'd like. What subject interests you today?"
        elif any(word in message_lower for word in ['help', 'stuck', 'confused']):
            ai_response = "Don't worry, that's completely normal when learning! Let's break it down step by step. What specific part would you like me to explain?"
        elif any(word in message_lower for word in ['math', 'mathematics', 'algebra', 'calculus']):
            ai_response = "Math is such a powerful subject! I'd love to help you with that. Are you working on a specific problem or concept?"
        elif any(word in message_lower for word in ['programming', 'code', 'python', 'javascript']):
            ai_response = "Programming is amazing! It's like learning a new language that lets you create incredible things. What programming topic interests you?"
        elif any(word in message_lower for word in ['science', 'physics', 'chemistry', 'biology']):
            ai_response = "Science helps us understand how the world works! It's fascinating. Which area of science would you like to explore?"
        else:
            ai_response = "That's a great question! I'm here to help you learn and understand better. Can you tell me more about what you'd like to know?"
    
    # Award points for chat interaction
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, total_points) VALUES (?, 0)
    ''', (user_id,))
    
    cursor.execute('''
        UPDATE users SET total_points = total_points + 2 WHERE id = ?
    ''', (user_id,))
    
    # Get updated user data
    cursor.execute('SELECT total_points, level FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        total_points, level = result
        new_level = max(1, total_points // 100 + 1)
        if new_level != level:
            cursor.execute('UPDATE users SET level = ? WHERE id = ?', (new_level, user_id))
            level = new_level
    else:
        total_points, level = 2, 1
    
    conn.commit()
    conn.close()
    
    # Emit AI response
    emit('ai_response', {
        'message': ai_response,
        'timestamp': datetime.now().isoformat(),
        'user_data': {
            'points': total_points,
            'level': level,
            'search_count': len(session.get('recent_searches', []))
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Futuristic AI Learning Assistant...")
    print("🌐 URL: http://localhost:5003")
    print("🤖 Enhanced Features:")
    print("   ✨ Dynamic course popups")
    print("   🧠 AI recommendations (Ollama)")
    print("   💬 Real-time AI chat")
    print("   🎤 Voice search")
    print("   📊 Progress tracking")
    print("   🎮 Gamification system")
    print("   🌓 Dark/Light mode")
    print("")
    
    if check_ollama_connection():
        print("✅ Ollama AI is connected and ready!")
    else:
        print("⚠️  Ollama not detected - using smart fallbacks")
    
    print("🔄 Press Ctrl+C to stop the server")
    
    # Run with SocketIO for real-time features
    socketio.run(app, debug=True, host='0.0.0.0', port=5003) 