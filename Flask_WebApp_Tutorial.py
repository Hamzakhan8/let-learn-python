# ==========================================
# COMPLETE FLASK WEB APP TUTORIAL
# ==========================================
# Learn how to build web applications with Python Flask

"""
WHAT IS FLASK?
==============
Flask is a lightweight Python web framework that makes it easy to build web applications.
It's perfect for beginners and powerful enough for complex applications.

WHAT YOU'LL LEARN:
==================
1. Flask basics and setup
2. Routes and URL handling
3. Templates and HTML rendering
4. Forms and user input
5. Static files (CSS, JS, images)
6. Sessions and data storage
7. API endpoints and JSON
8. Deployment basics
"""

# ==========================================
# STEP 1: INSTALLATION AND SETUP
# ==========================================

"""
1. Install Flask:
   pip install flask

2. Create your project structure:
   my_web_app/
   ├── app.py              # Main application file
   ├── templates/          # HTML templates
   │   └── index.html
   ├── static/            # CSS, JS, images
   │   ├── style.css
   │   └── script.js
   └── requirements.txt   # Dependencies
"""

# ==========================================
# STEP 2: BASIC FLASK APP
# ==========================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

# ==========================================
# STEP 3: BASIC ROUTES
# ==========================================

@app.route('/')
def home():
    """
    Home page route - handles GET requests to '/'
    Returns: HTML content or template
    """
    return """
    <h1>Welcome to My Flask App!</h1>
    <p>This is a basic Flask web application.</p>
    <a href="/about">About Page</a> | 
    <a href="/contact">Contact</a> |
    <a href="/demo">Demo Features</a>
    """

@app.route('/about')
def about():
    """
    About page - static content
    """
    return """
    <h1>About Us</h1>
    <p>This is the about page of our Flask application.</p>
    <a href="/">Back to Home</a>
    """

# ==========================================
# STEP 4: DYNAMIC ROUTES WITH PARAMETERS
# ==========================================

@app.route('/user/<username>')
def user_profile(username):
    """
    Dynamic route with URL parameter
    Example: /user/john will show John's profile
    """
    return f"""
    <h1>User Profile: {username}</h1>
    <p>Welcome, {username}!</p>
    <a href="/">Back to Home</a>
    """

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    Route with integer parameter
    Example: /post/123 will show post with ID 123
    """
    return f"""
    <h1>Post #{post_id}</h1>
    <p>This is the content of post number {post_id}</p>
    <a href="/">Back to Home</a>
    """

# ==========================================
# STEP 5: HANDLING DIFFERENT HTTP METHODS
# ==========================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handle both GET and POST requests
    GET: Show the contact form
    POST: Process form submission
    """
    if request.method == 'GET':
        # Show contact form
        return """
        <h1>Contact Us</h1>
        <form method="POST">
            <p>
                <label>Name:</label><br>
                <input type="text" name="name" required>
            </p>
            <p>
                <label>Email:</label><br>
                <input type="email" name="email" required>
            </p>
            <p>
                <label>Message:</label><br>
                <textarea name="message" rows="5" cols="40" required></textarea>
            </p>
            <p>
                <button type="submit">Send Message</button>
            </p>
        </form>
        <a href="/">Back to Home</a>
        """
    
    elif request.method == 'POST':
        # Process form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # In real app, you'd save to database or send email
        return f"""
        <h1>Thank You!</h1>
        <p>Thank you {name}, your message has been received!</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong> {message}</p>
        <a href="/">Back to Home</a>
        """

# ==========================================
# STEP 6: TEMPLATES AND HTML RENDERING
# ==========================================

@app.route('/demo')
def demo_features():
    """
    Demonstrate template rendering with data
    """
    # Sample data to pass to template
    user_data = {
        'name': 'Hamza',
        'age': 25,
        'skills': ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript'],
        'projects': [
            {'name': 'Coin Flip Predictor', 'status': 'Complete'},
            {'name': 'Todo App', 'status': 'In Progress'},
            {'name': 'Blog System', 'status': 'Planning'}
        ]
    }
    
    # If templates/demo.html exists, render it with data
    # Otherwise, show inline HTML
    return f"""
    <h1>Demo Features</h1>
    <h2>User Information</h2>
    <p><strong>Name:</strong> {user_data['name']}</p>
    <p><strong>Age:</strong> {user_data['age']}</p>
    
    <h2>Skills</h2>
    <ul>
        {''.join([f'<li>{skill}</li>' for skill in user_data['skills']])}
    </ul>
    
    <h2>Projects</h2>
    <ul>
        {''.join([f'<li>{project["name"]} - {project["status"]}</li>' for project in user_data['projects']])}
    </ul>
    
    <p><a href="/sessions">Try Sessions Demo</a></p>
    <p><a href="/api/data">Try API Demo</a></p>
    <a href="/">Back to Home</a>
    """

# ==========================================
# STEP 7: SESSIONS (USER DATA STORAGE)
# ==========================================

@app.route('/sessions')
def sessions_demo():
    """
    Demonstrate session usage for storing user data
    """
    # Initialize visit counter
    if 'visits' not in session:
        session['visits'] = 0
    
    session['visits'] += 1
    
    return f"""
    <h1>Sessions Demo</h1>
    <p>You have visited this page {session['visits']} time(s)!</p>
    <p><a href="/sessions">Refresh to increment</a></p>
    <p><a href="/clear-session">Clear Session</a></p>
    <a href="/">Back to Home</a>
    """

@app.route('/clear-session')
def clear_session():
    """
    Clear session data
    """
    session.clear()
    return """
    <h1>Session Cleared!</h1>
    <p>All session data has been cleared.</p>
    <p><a href="/sessions">Go back to sessions demo</a></p>
    <a href="/">Back to Home</a>
    """

# ==========================================
# STEP 8: API ENDPOINTS (JSON RESPONSES)
# ==========================================

@app.route('/api/data')
def api_data():
    """
    API endpoint that returns JSON data
    Perfect for AJAX calls or mobile apps
    """
    sample_data = {
        'status': 'success',
        'message': 'This is API data from Flask!',
        'data': {
            'users': [
                {'id': 1, 'name': 'Alice', 'role': 'Admin'},
                {'id': 2, 'name': 'Bob', 'role': 'User'},
                {'id': 3, 'name': 'Charlie', 'role': 'Moderator'}
            ],
            'total_users': 3,
            'server_time': '2025-06-11 15:30:00'
        }
    }
    
    return jsonify(sample_data)

@app.route('/api/echo', methods=['POST'])
def api_echo():
    """
    API endpoint that echoes back posted JSON data
    Great for testing API calls
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if data:
            return jsonify({
                'status': 'success',
                'message': 'Data received successfully',
                'received_data': data,
                'data_type': type(data).__name__
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing request: {str(e)}'
        }), 500

# ==========================================
# STEP 9: ERROR HANDLING
# ==========================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error page
    """
    return """
    <h1>Page Not Found (404)</h1>
    <p>Sorry, the page you're looking for doesn't exist.</p>
    <a href="/">Go back to Home</a>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """
    Custom 500 error page
    """
    return """
    <h1>Internal Server Error (500)</h1>
    <p>Something went wrong on our end. Please try again later.</p>
    <a href="/">Go back to Home</a>
    """, 500

# ==========================================
# STEP 10: ADVANCED FEATURES DEMO
# ==========================================

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """
    Simple calculator web app
    """
    if request.method == 'GET':
        return """
        <h1>Web Calculator</h1>
        <form method="POST">
            <p>
                <label>First Number:</label><br>
                <input type="number" step="any" name="num1" required>
            </p>
            <p>
                <label>Operation:</label><br>
                <select name="operation" required>
                    <option value="add">Addition (+)</option>
                    <option value="subtract">Subtraction (-)</option>
                    <option value="multiply">Multiplication (×)</option>
                    <option value="divide">Division (÷)</option>
                </select>
            </p>
            <p>
                <label>Second Number:</label><br>
                <input type="number" step="any" name="num2" required>
            </p>
            <p>
                <button type="submit">Calculate</button>
            </p>
        </form>
        <a href="/">Back to Home</a>
        """
    
    elif request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            if operation == 'add':
                result = num1 + num2
                symbol = '+'
            elif operation == 'subtract':
                result = num1 - num2
                symbol = '-'
            elif operation == 'multiply':
                result = num1 * num2
                symbol = '×'
            elif operation == 'divide':
                if num2 == 0:
                    return """
                    <h1>Error!</h1>
                    <p>Cannot divide by zero!</p>
                    <a href="/calculator">Try Again</a>
                    """
                result = num1 / num2
                symbol = '÷'
            else:
                return "Invalid operation!", 400
            
            return f"""
            <h1>Calculator Result</h1>
            <p><strong>{num1} {symbol} {num2} = {result}</strong></p>
            <p><a href="/calculator">Calculate Again</a></p>
            <a href="/">Back to Home</a>
            """
            
        except ValueError:
            return """
            <h1>Error!</h1>
            <p>Please enter valid numbers!</p>
            <a href="/calculator">Try Again</a>
            """

# ==========================================
# STEP 11: RUNNING THE APPLICATION
# ==========================================

if __name__ == '__main__':
    print("🌐 Starting Flask Web App Tutorial...")
    print("📱 Open your browser and go to:")
    print("   - Home: http://localhost:5000")
    print("   - About: http://localhost:5000/about")
    print("   - Contact: http://localhost:5000/contact")
    print("   - Demo: http://localhost:5000/demo")
    print("   - Calculator: http://localhost:5000/calculator")
    print("   - API: http://localhost:5000/api/data")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)

# ==========================================
# STEP 12: NEXT STEPS FOR REAL APPS
# ==========================================

"""
NEXT STEPS FOR PRODUCTION APPS:
===============================

1. TEMPLATES:
   - Create templates/ folder
   - Use Jinja2 templating
   - Separate HTML from Python code

2. STATIC FILES:
   - Create static/ folder
   - Add CSS, JavaScript, images
   - Use url_for('static', filename='...')

3. DATABASE:
   - Use SQLAlchemy or similar
   - Store data persistently
   - Handle user accounts

4. FORMS:
   - Use Flask-WTF for form validation
   - Add CSRF protection
   - Handle file uploads

5. AUTHENTICATION:
   - User login/logout
   - Password hashing
   - Session management

6. DEPLOYMENT:
   - Use production WSGI server (Gunicorn)
   - Set up proper hosting (Heroku, PythonAnywhere)
   - Configure environment variables

7. SECURITY:
   - Use HTTPS
   - Validate all inputs
   - Protect against SQL injection

USEFUL FLASK EXTENSIONS:
========================
- Flask-SQLAlchemy: Database ORM
- Flask-WTF: Form handling
- Flask-Login: User authentication
- Flask-Mail: Email functionality
- Flask-Admin: Admin interface

LEARNING RESOURCES:
==================
- Flask Documentation: https://flask.palletsprojects.com/
- Flask Mega-Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- Real Python Flask tutorials
""" 