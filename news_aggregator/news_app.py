# ==========================================
# NEWS AGGREGATOR WEB APPLICATION
# ==========================================
# A Flask web app that fetches news from RSS feeds
# Users can select topics and view specific news articles

import feedparser
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse
import time

# Create Flask application
app = Flask(__name__)
app.secret_key = 'news-aggregator-secret-key'

# ==========================================
# NEWS SOURCES AND RSS FEEDS
# ==========================================

NEWS_SOURCES = {
    'technology': {
        'name': 'Technology',
        'feeds': [
            {
                'name': 'TechCrunch',
                'url': 'https://techcrunch.com/feed/',
                'description': 'Latest technology news and startups'
            },
            {
                'name': 'The Verge',
                'url': 'https://www.theverge.com/rss/index.xml',
                'description': 'Technology, science, art, and culture'
            },
            {
                'name': 'Ars Technica',
                'url': 'http://feeds.arstechnica.com/arstechnica/index',
                'description': 'In-depth technology articles'
            },
            {
                'name': 'Wired',
                'url': 'https://www.wired.com/feed/rss',
                'description': 'How technology changes everything'
            }
        ]
    },
    'programming': {
        'name': 'Programming',
        'feeds': [
            {
                'name': 'Dev.to',
                'url': 'https://dev.to/feed',
                'description': 'Developer community articles'
            },
            {
                'name': 'Hacker News',
                'url': 'https://hnrss.org/frontpage',
                'description': 'Social news for developers'
            },
            {
                'name': 'Stack Overflow Blog',
                'url': 'https://stackoverflow.blog/feed/',
                'description': 'Programming insights and tutorials'
            },
            {
                'name': 'GitHub Blog',
                'url': 'https://github.blog/feed/',
                'description': 'Updates from GitHub'
            }
        ]
    },
    'science': {
        'name': 'Science',
        'feeds': [
            {
                'name': 'Science Daily',
                'url': 'https://www.sciencedaily.com/rss/all.xml',
                'description': 'Latest science news'
            },
            {
                'name': 'NASA News',
                'url': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
                'description': 'Space and NASA updates'
            },
            {
                'name': 'New Scientist',
                'url': 'https://www.newscientist.com/feed/home/',
                'description': 'Science and technology news'
            }
        ]
    },
    'business': {
        'name': 'Business',
        'feeds': [
            {
                'name': 'BBC Business',
                'url': 'http://feeds.bbci.co.uk/news/business/rss.xml',
                'description': 'BBC Business news'
            },
            {
                'name': 'Reuters Business',
                'url': 'https://feeds.reuters.com/reuters/businessNews',
                'description': 'Global business news'
            },
            {
                'name': 'Forbes',
                'url': 'https://www.forbes.com/real-time/feed2/',
                'description': 'Business and financial news'
            }
        ]
    },
    'world': {
        'name': 'World News',
        'feeds': [
            {
                'name': 'BBC World',
                'url': 'http://feeds.bbci.co.uk/news/world/rss.xml',
                'description': 'BBC World news'
            },
            {
                'name': 'Reuters World',
                'url': 'https://feeds.reuters.com/Reuters/worldNews',
                'description': 'Global news coverage'
            },
            {
                'name': 'Al Jazeera',
                'url': 'https://www.aljazeera.com/xml/rss/all.xml',
                'description': 'International news'
            }
        ]
    }
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def fetch_rss_feed(feed_url, max_entries=10):
    """
    Fetch and parse RSS feed
    Returns: List of articles or empty list if error
    """
    try:
        # Set timeout and user agent for better compatibility
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)
        
        articles = []
        
        # Process each entry (limit to max_entries)
        for entry in feed.entries[:max_entries]:
            # Clean and format the article data
            article = {
                'title': clean_text(entry.get('title', 'No Title')),
                'summary': clean_text(entry.get('summary', entry.get('description', 'No summary available'))),
                'link': entry.get('link', '#'),
                'published': format_date(entry.get('published', '')),
                'source': feed.feed.get('title', 'Unknown Source'),
                'author': entry.get('author', 'Unknown Author')
            }
            
            # Extract image if available
            if hasattr(entry, 'media_thumbnail'):
                article['image'] = entry.media_thumbnail[0]['url']
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                for enc in entry.enclosures:
                    if 'image' in enc.type:
                        article['image'] = enc.href
                        break
            else:
                article['image'] = None
            
            articles.append(article)
        
        return articles
    
    except Exception as e:
        print(f"Error fetching RSS feed {feed_url}: {str(e)}")
        return []

def clean_text(text):
    """
    Clean HTML tags and extra whitespace from text
    """
    if not text:
        return ""
    
    # Remove HTML tags
    clean = re.sub('<.*?>', '', text)
    
    # Remove extra whitespace
    clean = ' '.join(clean.split())
    
    # Limit length for summaries
    if len(clean) > 300:
        clean = clean[:300] + "..."
    
    return clean

def format_date(date_string):
    """
    Format date string to readable format
    """
    if not date_string:
        return "Unknown Date"
    
    try:
        # Parse the date string (RSS feeds use various formats)
        parsed_date = feedparser._parse_date(date_string)
        if parsed_date:
            dt = datetime(*parsed_date[:6])
            return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        pass
    
    return date_string

def get_articles_by_topic(topic, max_per_source=5):
    """
    Fetch articles for a specific topic from all its RSS sources
    """
    if topic not in NEWS_SOURCES:
        return []
    
    all_articles = []
    
    for feed_info in NEWS_SOURCES[topic]['feeds']:
        print(f"Fetching from {feed_info['name']}...")
        articles = fetch_rss_feed(feed_info['url'], max_per_source)
        
        # Add source name to each article
        for article in articles:
            article['feed_name'] = feed_info['name']
            article['feed_description'] = feed_info['description']
        
        all_articles.extend(articles)
    
    # Sort by published date (newest first)
    try:
        all_articles.sort(key=lambda x: x['published'], reverse=True)
    except:
        pass  # If sorting fails, just return unsorted
    
    return all_articles

# ==========================================
# FLASK ROUTES
# ==========================================

@app.route('/')
def home():
    """
    Home page - show available news topics
    """
    # Get user's favorite topics from session
    favorites = session.get('favorites', [])
    
    return render_template('index.html', 
                         topics=NEWS_SOURCES,
                         favorites=favorites)

@app.route('/topic/<topic_name>')
def show_topic(topic_name):
    """
    Display news articles for a specific topic
    """
    if topic_name not in NEWS_SOURCES:
        return render_template('error.html', 
                             message=f"Topic '{topic_name}' not found"), 404
    
    # Get articles for this topic
    articles = get_articles_by_topic(topic_name)
    topic_info = NEWS_SOURCES[topic_name]
    
    # Store viewed topic in session
    if 'recent_topics' not in session:
        session['recent_topics'] = []
    
    if topic_name not in session['recent_topics']:
        session['recent_topics'].insert(0, topic_name)
        session['recent_topics'] = session['recent_topics'][:5]  # Keep only 5 recent
    
    return render_template('topic.html',
                         topic_name=topic_name,
                         topic_info=topic_info,
                         articles=articles,
                         total_articles=len(articles))

@app.route('/article')
def show_article():
    """
    Display a specific article (redirects to external link)
    """
    article_url = request.args.get('url')
    if not article_url:
        return redirect(url_for('home'))
    
    # In a real app, you might want to track article views
    # For now, just redirect to the external article
    return redirect(article_url)

@app.route('/search')
def search():
    """
    Search articles across all topics
    """
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return render_template('search.html', 
                             query='',
                             results=[],
                             total=0)
    
    # Search across all topics
    all_results = []
    
    for topic_name in NEWS_SOURCES.keys():
        articles = get_articles_by_topic(topic_name, max_per_source=3)
        
        # Filter articles that match search query
        for article in articles:
            if (query in article['title'].lower() or 
                query in article['summary'].lower()):
                article['topic'] = topic_name
                article['topic_name'] = NEWS_SOURCES[topic_name]['name']
                all_results.append(article)
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_results = []
    for article in all_results:
        if article['title'] not in seen_titles:
            seen_titles.add(article['title'])
            unique_results.append(article)
    
    return render_template('search.html',
                         query=query,
                         results=unique_results,
                         total=len(unique_results))

@app.route('/favorites')
def favorites():
    """
    Show user's favorite topics
    """
    user_favorites = session.get('favorites', [])
    favorite_topics = {k: v for k, v in NEWS_SOURCES.items() if k in user_favorites}
    
    return render_template('favorites.html',
                         favorite_topics=favorite_topics)

@app.route('/api/toggle_favorite', methods=['POST'])
def toggle_favorite():
    """
    Add/remove topic from favorites
    """
    topic = request.json.get('topic')
    
    if topic not in NEWS_SOURCES:
        return jsonify({'error': 'Invalid topic'}), 400
    
    if 'favorites' not in session:
        session['favorites'] = []
    
    if topic in session['favorites']:
        session['favorites'].remove(topic)
        is_favorite = False
    else:
        session['favorites'].append(topic)
        is_favorite = True
    
    return jsonify({
        'success': True,
        'is_favorite': is_favorite,
        'topic': topic
    })

@app.route('/api/refresh_topic/<topic_name>')
def refresh_topic(topic_name):
    """
    API endpoint to refresh articles for a topic
    """
    if topic_name not in NEWS_SOURCES:
        return jsonify({'error': 'Invalid topic'}), 400
    
    articles = get_articles_by_topic(topic_name)
    
    return jsonify({
        'topic': topic_name,
        'articles': articles,
        'count': len(articles),
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/trending')
def trending():
    """
    Show trending/most recent articles across all topics
    """
    all_articles = []
    
    # Get a few articles from each topic
    for topic_name in NEWS_SOURCES.keys():
        articles = get_articles_by_topic(topic_name, max_per_source=2)
        for article in articles:
            article['topic'] = topic_name
            article['topic_name'] = NEWS_SOURCES[topic_name]['name']
        all_articles.extend(articles)
    
    # Sort by most recent
    try:
        all_articles.sort(key=lambda x: x['published'], reverse=True)
    except:
        pass
    
    # Take top 20 most recent
    trending_articles = all_articles[:20]
    
    return render_template('trending.html',
                         articles=trending_articles,
                         total=len(trending_articles))

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html',
                         message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html',
                         message="Internal server error"), 500

# ==========================================
# RUN THE APPLICATION
# ==========================================

if __name__ == '__main__':
    print("📰 Starting News Aggregator Web App...")
    print("🌐 Open your browser and go to: http://localhost:5001")
    print("📱 Available features:")
    print("   - Browse news by topic")
    print("   - Search articles")
    print("   - Save favorite topics") 
    print("   - View trending news")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Run on port 5001 to avoid conflict with coin flip app
    app.run(debug=True, host='0.0.0.0', port=5001) 