# ==========================================
# FUTURISTIC AI-POWERED STUDENT LEARNING ASSISTANT
# ==========================================
# Advanced Flask web app with:
# - Dynamic course popups
# - Ollama AI recommendations 
# - Real-time AI chat
# - Voice search
# - Progress tracking
# - Gamification
# - Dark/Light mode
# - And many more futuristic features!

import os
import re
import json
import random
import requests
import asyncio
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import wikipedia
import urllib.parse
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask application with SocketIO for real-time features
app = Flask(__name__)
app.secret_key = 'futuristic-ai-learning-assistant-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================================
# OLLAMA AI CONFIGURATION
# ==========================================

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"  # You can change this to any model you have installed

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_ai_recommendation(query, user_profile=None):
    """Get AI-powered course recommendations from Ollama"""
    try:
        if not check_ollama_connection():
            return get_fallback_recommendation(query)
        
        prompt = f"""
        You are an expert educational AI assistant. A student is asking about: "{query}"
        
        Please provide:
        1. A personalized learning recommendation
        2. Suggested course structure (3-5 main topics)
        3. Difficulty level assessment
        4. Estimated learning time
        5. Prerequisites (if any)
        6. Fun facts or motivation
        
        User profile: {user_profile if user_profile else 'Beginner level, general interest'}
        
        Format your response as a JSON object with keys: recommendation, course_structure, difficulty, time_estimate, prerequisites, fun_facts
        """
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return parse_ai_response(result.get('response', ''))
        else:
            return get_fallback_recommendation(query)
            
    except Exception as e:
        print(f"AI recommendation error: {e}")
        return get_fallback_recommendation(query)

def parse_ai_response(response_text):
    """Parse AI response and extract structured data"""
    try:
        # Try to extract JSON from the response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Fallback: create structured response from text
            return {
                "recommendation": response_text[:200] + "...",
                "course_structure": ["Introduction", "Core Concepts", "Practice", "Advanced Topics"],
                "difficulty": "Intermediate",
                "time_estimate": "2-4 weeks",
                "prerequisites": "Basic knowledge helpful",
                "fun_facts": "This is an exciting field with many applications!"
            }
    except:
        return get_fallback_recommendation("general")

def get_fallback_recommendation(query):
    """Fallback recommendations when AI is not available"""
    return {
        "recommendation": f"Great choice! {query} is a fantastic subject to learn. Start with the basics and gradually build your understanding.",
        "course_structure": ["Introduction & Basics", "Core Concepts", "Practical Applications", "Advanced Topics", "Real-world Projects"],
        "difficulty": "Beginner to Intermediate",
        "time_estimate": "2-6 weeks depending on pace",
        "prerequisites": "Curiosity and dedication to learn!",
        "fun_facts": f"Did you know that {query} has applications in many different fields and industries?"
    }

# ==========================================
# DATABASE SETUP
# ==========================================

def init_database():
    """Initialize SQLite database for user progress and analytics"""
    conn = sqlite3.connect('learning_assistant.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            learning_streak INTEGER DEFAULT 0,
            total_points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
    ''')
    
    # Learning progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            topic TEXT,
            progress_percentage REAL DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            completed_modules TEXT,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Search analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            result_clicked BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            achievement_type TEXT,
            achievement_name TEXT,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# ==========================================
# ENHANCED SUBJECT CATEGORIES
# ==========================================

SUBJECT_CATEGORIES = {
    'mathematics': {
        'name': 'Mathematics',
        'icon': 'fa-calculator',
        'keywords': ['math', 'algebra', 'geometry', 'calculus', 'statistics', 'trigonometry', 'arithmetic'],
        'color': '#10b981',
        'courses': ['Basic Arithmetic', 'Algebra Fundamentals', 'Geometry', 'Calculus', 'Statistics', 'Linear Algebra'],
        'difficulty_levels': ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    },
    'science': {
        'name': 'Science',
        'icon': 'fa-atom',
        'keywords': ['physics', 'chemistry', 'biology', 'astronomy', 'geology', 'anatomy'],
        'color': '#06b6d4',
        'courses': ['Physics Basics', 'Chemistry Fundamentals', 'Biology', 'Earth Science', 'Astronomy', 'Environmental Science'],
        'difficulty_levels': ['Beginner', 'Intermediate', 'Advanced', 'Research Level']
    },
    'programming': {
        'name': 'Programming',
        'icon': 'fa-code',
        'keywords': ['python', 'javascript', 'java', 'programming', 'coding', 'software', 'algorithm'],
        'color': '#8b5cf6',
        'courses': ['Python Basics', 'Web Development', 'Data Structures', 'Algorithms', 'Machine Learning', 'Mobile Apps'],
        'difficulty_levels': ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    },
    'history': {
        'name': 'History',
        'icon': 'fa-landmark',
        'keywords': ['history', 'historical', 'civilization', 'ancient', 'medieval', 'war', 'empire'],
        'color': '#f59e0b',
        'courses': ['Ancient History', 'Medieval Times', 'Modern History', 'World Wars', 'Cultural History', 'Art History'],
        'difficulty_levels': ['Basic', 'Intermediate', 'Advanced', 'Scholar']
    },
    'language': {
        'name': 'Language Arts',
        'icon': 'fa-language',
        'keywords': ['grammar', 'writing', 'literature', 'english', 'poetry', 'essay', 'reading'],
        'color': '#ec4899',
        'courses': ['Grammar Basics', 'Creative Writing', 'Literature Analysis', 'Poetry', 'Essay Writing', 'Public Speaking'],
        'difficulty_levels': ['Beginner', 'Intermediate', 'Advanced', 'Professional']
    },
    'geography': {
        'name': 'Geography',
        'icon': 'fa-globe-americas',
        'keywords': ['geography', 'countries', 'capitals', 'continents', 'maps', 'climate', 'population'],
        'color': '#64748b',
        'courses': ['World Geography', 'Physical Geography', 'Human Geography', 'Climate Studies', 'Cultural Geography'],
        'difficulty_levels': ['Basic', 'Intermediate', 'Advanced', 'Expert']
    }
}

# ==========================================
# ENHANCED EDUCATIONAL CONTENT
# ==========================================

COURSE_DATABASE = {
    'python': {
        'title': 'Python Programming Mastery',
        'description': 'Complete Python course from beginner to advanced',
        'modules': [
            'Python Basics & Syntax',
            'Data Types & Variables',
            'Control Structures',
            'Functions & Modules',
            'Object-Oriented Programming',
            'File Handling & APIs',
            'Web Development with Flask',
            'Data Science & ML'
        ],
        'duration': '8-12 weeks',
        'difficulty': 'Beginner to Advanced',
        'rating': 4.8,
        'students': 15420,
        'videos': [
        {
            'id': 'rfscVS0vtbw',
                'title': 'Python Full Course for Beginners',
                'duration': '4:26:53',
                'thumbnail': 'https://i.ytimg.com/vi/rfscVS0vtbw/maxresdefault.jpg'
            }
        ]
    },
    'mathematics': {
        'title': 'Mathematics Complete Course',
        'description': 'Master mathematics from basics to advanced calculus',
        'modules': [
            'Number Systems',
            'Algebra Fundamentals',
            'Geometry & Trigonometry',
            'Calculus Basics',
            'Statistics & Probability',
            'Linear Algebra',
            'Differential Equations',
            'Applied Mathematics'
        ],
        'duration': '10-16 weeks',
        'difficulty': 'All Levels',
        'rating': 4.9,
        'students': 23150,
        'videos': []
    }
}

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def get_user_id():
    """Get current user ID from session"""
    return session.get('user_id', f"guest_{random.randint(1000, 9999)}")

def log_search_analytics(query, user_id=None):
    """Log search queries for analytics"""
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO search_analytics (user_id, query) VALUES (?, ?)",
            (user_id or get_user_id(), query)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Analytics logging error: {e}")

def update_learning_progress(user_id, topic, progress=10):
    """Update user's learning progress"""
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        
        # Check if progress exists
        cursor.execute(
            "SELECT progress_percentage FROM learning_progress WHERE user_id = ? AND topic = ?",
            (user_id, topic)
        )
        existing = cursor.fetchone()
        
        if existing:
            new_progress = min(100, existing[0] + progress)
            cursor.execute(
                "UPDATE learning_progress SET progress_percentage = ?, last_accessed = CURRENT_TIMESTAMP WHERE user_id = ? AND topic = ?",
                (new_progress, user_id, topic)
            )
        else:
            cursor.execute(
                "INSERT INTO learning_progress (user_id, topic, progress_percentage) VALUES (?, ?, ?)",
                (user_id, topic, progress)
            )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Progress update error: {e}")
        return False

def get_trending_topics():
    """Get trending topics based on recent searches"""
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT query, COUNT(*) as search_count 
            FROM search_analytics 
            WHERE timestamp > datetime('now', '-7 days')
            GROUP BY query 
            ORDER BY search_count DESC 
            LIMIT 10
        """)
        results = cursor.fetchall()
        conn.close()
        return [topic[0] for topic in results] if results else ['python', 'mathematics', 'science']
    except:
        return ['python', 'mathematics', 'science', 'history', 'geography']

# ==========================================
# FLASK ROUTES
# ==========================================

@app.route('/')
def home():
    """Enhanced home page with dynamic content"""
    user_id = get_user_id()
    trending_topics = get_trending_topics()
    recent_searches = session.get('recent_searches', [])
    
    # Get user progress if available
    user_progress = []
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topic, progress_percentage FROM learning_progress WHERE user_id = ? ORDER BY last_accessed DESC LIMIT 5",
            (user_id,)
        )
        user_progress = cursor.fetchall()
        conn.close()
    except:
        pass
    
    return render_template('index.html', 
                         categories=SUBJECT_CATEGORIES,
                         recent_searches=recent_searches,
                         trending_topics=trending_topics,
                         user_progress=user_progress,
                         user_id=user_id)

@app.route('/api/search_suggestions/<query>')
def search_suggestions(query):
    """Real-time search suggestions API"""
    suggestions = []
    
    # Add category matches
    for cat_key, cat_data in SUBJECT_CATEGORIES.items():
        if query.lower() in cat_data['name'].lower():
            suggestions.append({
                'text': cat_data['name'],
                'type': 'category',
                'icon': cat_data['icon']
            })
        
        # Add keyword matches
        for keyword in cat_data['keywords']:
            if query.lower() in keyword.lower():
                suggestions.append({
                    'text': keyword.title(),
                    'type': 'topic',
                    'icon': cat_data['icon']
                })
    
    # Add course matches
    for course_key, course_data in COURSE_DATABASE.items():
        if query.lower() in course_data['title'].lower():
            suggestions.append({
                'text': course_data['title'],
                'type': 'course',
                'icon': 'fa-play-circle'
            })
    
    return jsonify(suggestions[:10])

@app.route('/api/dynamic_search', methods=['POST'])
def dynamic_search():
    """Dynamic search with AI recommendations"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    user_id = get_user_id()
    log_search_analytics(query, user_id)
    
    # Get AI recommendation
    ai_recommendation = get_ai_recommendation(query)
    
    # Update session
    if 'recent_searches' not in session:
        session['recent_searches'] = []
    if query not in session['recent_searches']:
        session['recent_searches'].insert(0, query)
        session['recent_searches'] = session['recent_searches'][:10]
    
    # Get related content
    related_courses = []
    for course_key, course_data in COURSE_DATABASE.items():
        if any(keyword in query.lower() for keyword in [course_key] + course_data.get('keywords', [])):
            related_courses.append({
                'key': course_key,
                'title': course_data['title'],
                'description': course_data['description'],
                'modules': course_data['modules'][:3],  # First 3 modules
                'duration': course_data['duration'],
                'rating': course_data['rating'],
                'students': course_data['students']
            })
    
    # Update progress
    update_learning_progress(user_id, query, 5)
    
    return jsonify({
        'success': True,
        'query': query,
        'ai_recommendation': ai_recommendation,
        'related_courses': related_courses,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    """Real-time AI chat endpoint"""
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context', '')
    
    try:
        if not check_ollama_connection():
            return jsonify({
                'response': "I'm currently learning! Please try again in a moment. In the meantime, feel free to explore our courses and materials.",
                'suggestions': ['Browse Categories', 'View Trending Topics', 'Check Your Progress']
            })
        
        prompt = f"""
        You are a friendly, knowledgeable AI tutor. The student says: "{message}"
        Context: {context}
        
        Provide a helpful, encouraging response and suggest 2-3 follow-up actions or questions.
        Keep it conversational and educational.
        """
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.8}
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            
            return jsonify({
                'response': ai_response,
                'suggestions': ['Tell me more', 'Show examples', 'What should I learn next?']
            })
        else:
            raise Exception("AI service unavailable")
            
    except Exception as e:
        return jsonify({
            'response': "I'm having trouble connecting right now. Let me help you explore our available courses instead!",
            'suggestions': ['Browse Mathematics', 'Explore Programming', 'Check Science Topics']
        })

@app.route('/api/voice_search', methods=['POST'])
def voice_search():
    """Voice search processing endpoint"""
    data = request.get_json()
    transcript = data.get('transcript', '').strip()
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400
    
    # Process voice command
    if 'search for' in transcript.lower():
        query = transcript.lower().replace('search for', '').strip()
    elif 'learn about' in transcript.lower():
        query = transcript.lower().replace('learn about', '').strip()
    elif 'tell me about' in transcript.lower():
        query = transcript.lower().replace('tell me about', '').strip()
    else:
        query = transcript
    
    return jsonify({
        'success': True,
        'processed_query': query,
        'action': 'search'
    })

@app.route('/api/user_progress')
def user_progress():
    """Get user's learning progress"""
    user_id = get_user_id()
    
    try:
        conn = sqlite3.connect('learning_assistant.db')
        cursor = conn.cursor()
        
        # Get progress data
        cursor.execute("""
            SELECT topic, progress_percentage, time_spent, last_accessed 
            FROM learning_progress 
            WHERE user_id = ? 
            ORDER BY last_accessed DESC
        """, (user_id,))
        
        progress_data = []
        for row in cursor.fetchall():
            progress_data.append({
                'topic': row[0],
                'progress': row[1],
                'time_spent': row[2],
                'last_accessed': row[3]
            })
        
        # Get total stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_topics,
                AVG(progress_percentage) as avg_progress,
                SUM(time_spent) as total_time
            FROM learning_progress 
            WHERE user_id = ?
        """, (user_id,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'progress_data': progress_data,
            'stats': {
                'total_topics': stats[0] or 0,
                'avg_progress': round(stats[1] or 0, 1),
                'total_time': stats[2] or 0
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/toggle_theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark theme"""
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    
    return jsonify({
        'success': True,
        'theme': new_theme
    })

@app.route('/api/gamification/award_points', methods=['POST'])
def award_points():
    """Award points for learning activities"""
    data = request.get_json()
    user_id = get_user_id()
    activity = data.get('activity', '')
    points = data.get('points', 10)
    
    # Point system
    point_values = {
        'search': 5,
        'complete_module': 25,
        'daily_streak': 50,
        'course_completion': 100,
        'quiz_completion': 20
    }
    
    awarded_points = point_values.get(activity, points)
    
    # Update user points (simplified - in real app would update database)
    current_points = session.get('user_points', 0)
    session['user_points'] = current_points + awarded_points
    
    return jsonify({
        'success': True,
        'points_awarded': awarded_points,
        'total_points': session['user_points'],
        'achievement_unlocked': session['user_points'] % 100 == 0  # Unlock achievement every 100 points
    })

# ==========================================
# WEBSOCKET EVENTS FOR REAL-TIME FEATURES
# ==========================================

@socketio.on('join_study_room')
def on_join_study_room(data):
    """Join a collaborative study room"""
    room = data.get('room', 'general')
    user_id = get_user_id()
    join_room(room)
    emit('user_joined', {
        'user_id': user_id,
        'message': f'User {user_id} joined the study room'
    }, room=room)

@socketio.on('send_study_message')
def on_study_message(data):
    """Send message in study room"""
    room = data.get('room', 'general')
    message = data.get('message', '')
    user_id = get_user_id()
    
    emit('receive_study_message', {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, room=room)

@socketio.on('request_ai_help')
def on_ai_help_request(data):
    """Handle real-time AI help requests"""
    question = data.get('question', '')
    user_id = get_user_id()
    
    # Get AI response (simplified)
    ai_response = get_ai_recommendation(question)
    
    emit('ai_help_response', {
        'question': question,
        'response': ai_response,
        'user_id': user_id
    })

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message="Internal server error"), 500

# ==========================================
# RUN THE APPLICATION
# ==========================================

if __name__ == '__main__':
    print("🚀 Starting Futuristic AI Learning Assistant...")
    print("🌐 Open your browser and go to: http://localhost:5002")
    print("🤖 Features available:")
    print("   ✨ Dynamic course popups")
    print("   🧠 AI-powered recommendations (Ollama)")
    print("   💬 Real-time AI chat")
    print("   🎤 Voice search")
    print("   📊 Progress tracking")
    print("   🎮 Gamification system")
    print("   🌓 Dark/Light mode")
    print("   👥 Collaborative study rooms")
    print("   📈 Analytics dashboard")
    print("   🏆 Achievement system")
    print("")
    print("📋 Setup Instructions:")
    print("   1. Install Ollama: https://ollama.ai")
    print("   2. Run: ollama pull llama2")
    print("   3. Start Ollama service")
    print("   4. Enjoy the futuristic learning experience!")
    print("")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Check Ollama connection
    if check_ollama_connection():
        print("✅ Ollama AI is connected and ready!")
    else:
        print("⚠️  Ollama AI not detected - using fallback responses")
    
    # Run with SocketIO for real-time features
    socketio.run(app, debug=True, host='0.0.0.0', port=5002) 