# 🪙 Coin Flip Prediction Web App

## 🚀 How to Run the App

1. **Start the Web Server:**
   ```bash
   python coin_flip_app.py
   ```

2. **Open Your Browser:**
   - Go to: `http://localhost:5000`
   - Or: `http://127.0.0.1:5000`

3. **Stop the Server:**
   - Press `Ctrl+C` in the terminal

## 🎮 How to Use the App

### Features:
- **🪙 Flip Coin**: Click the button or press Spacebar to flip
- **🔮 Prediction System**: Shows "predictions" for next flip
- **📊 Statistics**: Tracks your flip history and patterns
- **🎯 Accuracy Tracking**: See how often predictions are "correct"
- **🔄 Reset**: Clear all data and start fresh

### Controls:
- **Click** the coin to flip it
- **Spacebar** to flip (keyboard shortcut)
- **Flip Coin** button to flip
- **Reset Stats** button to clear all data

## 🧠 How the "Prediction" Works

**Important Note**: Real coin flips are completely random and cannot be predicted!

Our app uses fun "prediction" algorithms for entertainment:

1. **Pattern Detection**: Looks at last 5 flips
2. **Gambler's Fallacy**: If more heads recently, "predicts" tails
3. **Random Element**: Adds randomness to keep it interesting

## 📊 Statistics Explained

- **Total Flips**: How many times you've flipped
- **Heads/Tails Count**: Number and percentage of each
- **Longest Streak**: Longest sequence of same result
- **Current Streak**: Current sequence of same result
- **Prediction Accuracy**: How often our "predictions" match reality

## 🎯 Learning Concepts

This web app demonstrates several Python concepts:

### **Basic Level:**
- Variables and data types
- Functions and parameters
- Conditional statements (if/else)
- Loops and iteration
- Lists and data structures

### **Intermediate Level:**
- Web development with Flask
- HTML templates (Jinja2)
- JSON data handling
- Session management
- HTTP requests and responses

### **Advanced Level:**
- Client-server communication
- AJAX/Fetch API
- CSS animations
- JavaScript integration
- Responsive web design

## 🔧 Technical Details

### **Backend (Python/Flask):**
- `coin_flip_app.py` - Main application
- Routes: `/` (home), `/flip` (API), `/reset` (API)
- Session storage for user data
- JSON API responses

### **Frontend (HTML/CSS/JavaScript):**
- `templates/index.html` - User interface
- CSS animations for coin flipping
- JavaScript for interactivity
- Responsive design for mobile

### **Key Technologies:**
- **Flask**: Python web framework
- **Jinja2**: Template engine
- **HTML5**: Modern web structure
- **CSS3**: Styling and animations
- **JavaScript**: Client-side interactivity

## 🎨 Customization Ideas

Want to enhance the app? Try these:

1. **Add Sound Effects**: Coin flip sounds
2. **More Animations**: Better visual effects
3. **Different Coins**: Various coin designs
4. **Betting System**: Virtual currency
5. **Multiplayer**: Share results online
6. **AI Predictions**: More sophisticated algorithms
7. **Themes**: Dark mode, different colors
8. **Mobile App**: Convert to mobile app

## 🐛 Troubleshooting

**App won't start?**
- Make sure Flask is installed: `pip install flask`
- Check Python version: `python --version`
- Make sure you're in the right directory

**Can't access the website?**
- Check if the server is running
- Try `http://127.0.0.1:5000` instead
- Make sure port 5000 isn't blocked

**Browser shows errors?**
- Check browser console (F12)
- Clear browser cache
- Try a different browser

## 🎓 What You've Learned

By building this app, you've learned:

✅ **Python Web Development**
✅ **HTML/CSS/JavaScript Integration**
✅ **API Design and JSON**
✅ **Session Management**
✅ **Interactive User Interfaces**
✅ **Real-time Updates**
✅ **Responsive Design**
✅ **Statistical Analysis**

---

**Enjoy your coin flipping adventure! 🪙✨** 