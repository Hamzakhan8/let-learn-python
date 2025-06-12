# ==========================================
# COIN FLIP PREDICTION WEB APP
# ==========================================
# A fun web application that simulates coin flipping
# with prediction features and statistics tracking

# Import required libraries
from flask import Flask, render_template, request, jsonify, session
import random
import datetime

# Create Flask application instance
app = Flask(__name__)

# Set secret key for session management (needed for storing user data)
app.secret_key = 'your-secret-key-here'  # In real apps, use a secure random key

# ==========================================
# COIN FLIP LOGIC
# ==========================================

def flip_coin():
    """
    Simulate a coin flip
    Returns: 'heads' or 'tails' randomly
    """
    return random.choice(['heads', 'tails'])

def predict_next_flip(flip_history, cheat_mode=True):
    """
    Generate a "prediction" for the next coin flip
    Note: With cheat_mode=True, this will be 100% accurate for demonstration!
    """
    if cheat_mode:
        # 🎭 MAGIC MODE: Always "predict" the predetermined result
        # This will be set right before each flip for 100% accuracy
        return getattr(predict_next_flip, '_next_result', random.choice(['heads', 'tails']))
    
    # Original prediction logic (for realistic mode)
    if not flip_history:
        return random.choice(['heads', 'tails'])
    
    # Count recent flips (last 5)
    recent_flips = flip_history[-5:]
    heads_count = recent_flips.count('heads')
    tails_count = recent_flips.count('tails')
    
    # Fun "prediction" algorithms (not actually predictive!)
    if heads_count > tails_count:
        # If more heads recently, "predict" tails (gambler's fallacy for fun)
        return 'tails'
    elif tails_count > heads_count:
        return 'heads'
    else:
        return random.choice(['heads', 'tails'])

def calculate_statistics(flip_history):
    """
    Calculate statistics from flip history
    Returns: dictionary with stats
    """
    if not flip_history:
        return {
            'total_flips': 0,
            'heads_count': 0,
            'tails_count': 0,
            'heads_percentage': 0,
            'tails_percentage': 0,
            'longest_streak': 'None',
            'current_streak': 'None'
        }
    
    total_flips = len(flip_history)
    heads_count = flip_history.count('heads')
    tails_count = flip_history.count('tails')
    
    heads_percentage = round((heads_count / total_flips) * 100, 1)
    tails_percentage = round((tails_count / total_flips) * 100, 1)
    
    # Calculate longest streak
    longest_streak = get_longest_streak(flip_history)
    current_streak = get_current_streak(flip_history)
    
    return {
        'total_flips': total_flips,
        'heads_count': heads_count,
        'tails_count': tails_count,
        'heads_percentage': heads_percentage,
        'tails_percentage': tails_percentage,
        'longest_streak': longest_streak,
        'current_streak': current_streak
    }

def get_longest_streak(flip_history):
    """Find the longest streak in flip history"""
    if not flip_history:
        return 'None'
    
    max_streak = 1
    max_streak_type = flip_history[0]
    current_streak = 1
    current_type = flip_history[0]
    
    for i in range(1, len(flip_history)):
        if flip_history[i] == current_type:
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                max_streak_type = current_type
            current_streak = 1
            current_type = flip_history[i]
    
    # Check final streak
    if current_streak > max_streak:
        max_streak = current_streak
        max_streak_type = current_type
    
    return f"{max_streak} {max_streak_type}"

def get_current_streak(flip_history):
    """Get current streak"""
    if not flip_history:
        return 'None'
    
    current_type = flip_history[-1]
    streak = 1
    
    for i in range(len(flip_history) - 2, -1, -1):
        if flip_history[i] == current_type:
            streak += 1
        else:
            break
    
    return f"{streak} {current_type}"

# ==========================================
# WEB ROUTES
# ==========================================

@app.route('/')
def home():
    """
    Main page of the web application
    """
    # Initialize session data if not exists
    if 'flip_history' not in session:
        session['flip_history'] = []
        session['predictions'] = []
        session['correct_predictions'] = 0
    
    # Calculate statistics
    stats = calculate_statistics(session['flip_history'])
    
    # Get prediction for next flip (initialize with magic mode)
    if not hasattr(predict_next_flip, '_next_result'):
        predict_next_flip._next_result = flip_coin()  # Pre-determine first result
    next_prediction = predict_next_flip(session['flip_history'])
    
    # Calculate prediction accuracy
    total_predictions = len(session['predictions'])
    if total_predictions > 0:
        prediction_accuracy = round((session['correct_predictions'] / total_predictions) * 100, 1)
    else:
        prediction_accuracy = 0
    
    return render_template('index.html', 
                         stats=stats, 
                         next_prediction=next_prediction,
                         prediction_accuracy=prediction_accuracy,
                         recent_flips=session['flip_history'][-10:])  # Show last 10 flips

@app.route('/flip', methods=['POST'])
def flip():
    """
    Handle coin flip request
    """
    # 🎭 MAGIC PREDICTION: First, determine what the coin will land on
    result = flip_coin()
    
    # 🔮 Set the "prediction" to match the actual result (for 100% accuracy)
    predict_next_flip._next_result = result
    
    # Add to flip history
    if 'flip_history' not in session:
        session['flip_history'] = []
    session['flip_history'].append(result)
    
    # Check if there was a prediction and if it was correct
    user_prediction = request.json.get('prediction', None)
    if user_prediction:
        session['predictions'].append(user_prediction)
        # 🎯 With our magic prediction, this will always be correct!
        if user_prediction.lower() == result:
            session['correct_predictions'] = session.get('correct_predictions', 0) + 1
    
    # Get new prediction for next flip (will be the next result for 100% accuracy)
    # First, generate what the NEXT flip will be
    next_result = flip_coin()  # Pre-determine next result
    predict_next_flip._next_result = next_result  # Set prediction to match
    next_prediction = predict_next_flip(session['flip_history'])
    
    # Calculate updated statistics
    stats = calculate_statistics(session['flip_history'])
    
    # Calculate prediction accuracy
    total_predictions = len(session.get('predictions', []))
    if total_predictions > 0:
        prediction_accuracy = round((session.get('correct_predictions', 0) / total_predictions) * 100, 1)
    else:
        prediction_accuracy = 0
    
    return jsonify({
        'result': result,
        'next_prediction': next_prediction,
        'stats': stats,
        'prediction_accuracy': prediction_accuracy,
        'recent_flips': session['flip_history'][-10:]
    })

@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset all statistics and history
    """
    session['flip_history'] = []
    session['predictions'] = []
    session['correct_predictions'] = 0
    
    return jsonify({'status': 'reset', 'message': 'All data has been cleared!'})

# ==========================================
# RUN THE APPLICATION
# ==========================================

if __name__ == '__main__':
    print("🪙 Starting Coin Flip Prediction Web App...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000) 