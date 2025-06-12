# 📰 News Aggregator Web Application

A modern, responsive news aggregator built with Flask that fetches articles from multiple RSS feeds across different topics.

## 🌟 Features

### 📖 Topic-Based News Browsing
- **Technology**: Latest tech news from TechCrunch, The Verge, Ars Technica, and Wired
- **Programming**: Developer articles from Dev.to, Hacker News, Stack Overflow Blog, and GitHub Blog
- **Science**: Scientific discoveries from Science Daily, NASA, and New Scientist
- **Business**: Financial news from BBC Business, Reuters Business, and Forbes
- **World News**: Global coverage from BBC World, Reuters World, and Al Jazeera

### 🔍 Advanced Search
- Search across all topics and sources
- Real-time article filtering
- Search suggestions and popular queries
- Cross-topic search results

### ⭐ Personalization
- Favorite topics system
- Session-based preferences
- Recent topics tracking
- Personalized recommendations

### 📈 Trending News
- Cross-topic trending articles
- Real-time updates
- Hot article indicators
- Auto-refresh functionality

### 🎨 Modern UI/UX
- Responsive design for all devices
- Beautiful gradient backgrounds
- Smooth animations and transitions
- Keyboard shortcuts
- Loading states and error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection for RSS feeds

### Installation

1. **Navigate to the news aggregator directory**:
   ```bash
   cd news_aggregator
   ```

2. **Install required packages**:
   ```bash
   python -m pip install flask feedparser requests
   ```

3. **Run the application**:
   ```bash
   python news_app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5001
   ```

## 📁 Project Structure

```
news_aggregator/
├── news_app.py              # Main Flask application
├── templates/               # HTML templates
│   ├── index.html          # Home page with topic selection
│   ├── topic.html          # Topic-specific news articles
│   ├── search.html         # Search results page
│   ├── trending.html       # Trending news page
│   └── error.html          # Error page
├── static/                 # Static files (currently empty - CSS is inline)
└── README_News_Aggregator.md  # This documentation
```

## 🌐 Available Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with topic selection |
| `/topic/<topic_name>` | GET | View articles for specific topic |
| `/search` | GET | Search articles across all topics |
| `/trending` | GET | View trending articles |
| `/favorites` | GET | View user's favorite topics |
| `/api/toggle_favorite` | POST | Add/remove topic from favorites |
| `/api/refresh_topic/<topic>` | GET | Refresh articles for a topic |

## 📚 RSS Sources

### Technology Sources
- **TechCrunch**: Latest technology news and startups
- **The Verge**: Technology, science, art, and culture
- **Ars Technica**: In-depth technology articles
- **Wired**: How technology changes everything

### Programming Sources
- **Dev.to**: Developer community articles
- **Hacker News**: Social news for developers
- **Stack Overflow Blog**: Programming insights and tutorials
- **GitHub Blog**: Updates from GitHub

### Science Sources
- **Science Daily**: Latest science news
- **NASA News**: Space and NASA updates
- **New Scientist**: Science and technology news

### Business Sources
- **BBC Business**: BBC Business news
- **Reuters Business**: Global business news
- **Forbes**: Business and financial news

### World News Sources
- **BBC World**: BBC World news
- **Reuters World**: Global news coverage
- **Al Jazeera**: International news

## 🔧 Technical Features

### RSS Feed Processing
- **feedparser** library for robust RSS parsing
- HTML tag removal and text cleaning
- Date formatting and standardization
- Error handling for unavailable feeds
- Automatic retry mechanisms

### Session Management
- User preferences stored in session
- Favorite topics persistence
- Recent topics tracking
- Cross-page state management

### API Endpoints
- RESTful API for favorites management
- JSON responses for dynamic updates
- Real-time article refresh
- AJAX-powered interactions

### Performance Optimization
- Efficient RSS feed caching
- Parallel processing for multiple feeds
- Lazy loading of article content
- Optimized database-free operation

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + /` | Focus search box |
| `Ctrl + R` | Refresh current page |
| `Escape` | Go back to home |

## 🎯 Usage Examples

### 1. Browse Technology News
```
1. Go to http://localhost:5001
2. Click on "Technology" topic card
3. Browse latest tech articles
4. Click "Read Full Article" to open in new tab
```

### 2. Search for Specific Topics
```
1. Use search box on home page
2. Enter keywords like "AI", "Python", "cryptocurrency"
3. Browse cross-topic search results
4. Filter by clicking topic badges
```

### 3. Save Favorite Topics
```
1. Click "⭐ Add to Favorites" on any topic card
2. Access favorites via "⭐ Favorites" link
3. Quick access to preferred news sources
```

### 4. View Trending News
```
1. Click "📈 Trending" in navigation
2. See latest articles across all topics
3. Hot articles marked with 🔥 badge
4. Auto-refreshes every 10 minutes
```

## 🛠️ Customization

### Adding New RSS Sources

1. **Edit `news_app.py`**:
   ```python
   NEWS_SOURCES = {
       'your_topic': {
           'name': 'Your Topic Name',
           'feeds': [
               {
                   'name': 'Source Name',
                   'url': 'https://example.com/rss',
                   'description': 'Source description'
               }
           ]
       }
   }
   ```

2. **Update templates** to include new topic icons and descriptions

### Modifying UI Themes

1. **Edit CSS in templates** for color schemes
2. **Change gradient backgrounds** in body styles
3. **Customize animations** and transitions
4. **Add new icons** for topics

### Configuring Feed Limits

```python
# In news_app.py, modify these parameters:
max_per_source = 5  # Articles per RSS source
max_entries = 10    # Max entries to process
```

## 🔍 Troubleshooting

### Common Issues

1. **No articles loading**:
   - Check internet connection
   - Verify RSS feed URLs are accessible
   - Some feeds may have rate limiting

2. **Search not working**:
   - Ensure articles are loaded first
   - Try different search terms
   - Check if feeds are accessible

3. **Favorites not saving**:
   - Enable cookies in browser
   - Check session configuration
   - Try in incognito mode

4. **Slow loading**:
   - Some RSS feeds may be slow
   - Network connectivity issues
   - Try refreshing the page

### Debug Mode

Enable debug mode for development:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🚀 Advanced Features

### Auto-Refresh
- Articles auto-refresh every 5 minutes on topic pages
- Trending page refreshes every 10 minutes
- Manual refresh buttons available

### Responsive Design
- Mobile-optimized layouts
- Touch-friendly interactions
- Adaptive grid systems
- Scalable typography

### Error Handling
- Graceful RSS feed failures
- User-friendly error messages
- Automatic retry mechanisms
- Fallback content display

## 📊 Statistics

The application tracks:
- Total number of topics
- RSS sources per topic
- User's favorite topics
- Article counts per topic
- Real-time statistics display

## 🔮 Future Enhancements

Potential improvements:
- **Database Integration**: Store articles and user preferences
- **User Accounts**: Personal profiles and settings
- **Email Notifications**: Send digest emails
- **Social Sharing**: Share articles on social media
- **Article Bookmarking**: Save articles for later
- **Comment System**: User discussions
- **Mobile App**: Native mobile application
- **Push Notifications**: Real-time article alerts

## 📝 License

This project is open-source and available for educational purposes.

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create feature branches
3. Add new RSS sources
4. Improve UI/UX
5. Submit pull requests

## 📧 Support

For questions or support:
- Check troubleshooting section
- Review RSS feed documentation
- Test with different news sources
- Verify internet connectivity

---

**Happy News Reading! 📰✨** 