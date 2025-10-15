"""
Advanced news fetching from multiple sources.
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NewsAggregator:
    """Aggregate news from multiple sources."""
    
    def __init__(self, news_api_key: str = None, finnhub_api_key: str = None):
        self.news_api_key = news_api_key
        self.finnhub_api_key = finnhub_api_key
    
    def fetch_newsapi(self, ticker: str, days: int = 7) -> List[Dict]:
        """Fetch from NewsAPI.org."""
        if not self.news_api_key:
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            params = {
                'q': ticker,
                'from': from_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            news = []
            for article in articles[:10]:
                news.append({
                    'source': 'NewsAPI',
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'published_at': article.get('publishedAt'),
                    'sentiment': None  # Will be analyzed separately
                })
            
            return news
            
        except Exception as e:
            logger.error(f"Error fetching NewsAPI for {ticker}: {e}")
            return []
    
    def fetch_finnhub(self, ticker: str, days: int = 7) -> List[Dict]:
        """Fetch from Finnhub."""
        if not self.finnhub_api_key:
            return []
        
        try:
            url = "https://finnhub.io/api/v1/company-news"
            
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            params = {
                'symbol': ticker,
                'from': from_date,
                'to': to_date,
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            articles = response.json()
            
            news = []
            for article in articles[:10]:
                news.append({
                    'source': 'Finnhub',
                    'title': article.get('headline'),
                    'description': article.get('summary'),
                    'url': article.get('url'),
                    'published_at': datetime.fromtimestamp(article.get('datetime')).isoformat(),
                    'sentiment': article.get('sentiment')  # Finnhub provides sentiment
                })
            
            return news
            
        except Exception as e:
            logger.error(f"Error fetching Finnhub for {ticker}: {e}")
            return []
    
    def fetch_polygon(self, ticker: str, polygon_api_key: str, limit: int = 10) -> List[Dict]:
        """Fetch from Polygon.io."""
        if not polygon_api_key:
            return []
        
        try:
            url = f"https://api.polygon.io/v2/reference/news"
            
            params = {
                'ticker': ticker,
                'limit': limit,
                'apiKey': polygon_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('results', [])
            
            news = []
            for article in articles:
                news.append({
                    'source': 'Polygon',
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('article_url'),
                    'published_at': article.get('published_utc'),
                    'sentiment': None
                })
            
            return news
            
        except Exception as e:
            logger.error(f"Error fetching Polygon news for {ticker}: {e}")
            return []
    
    def aggregate_all(
        self,
        ticker: str,
        days: int = 7,
        polygon_api_key: str = None
    ) -> List[Dict]:
        """Aggregate news from all available sources."""
        all_news = []
        
        # Fetch from each source
        all_news.extend(self.fetch_newsapi(ticker, days))
        all_news.extend(self.fetch_finnhub(ticker, days))
        
        if polygon_api_key:
            all_news.extend(self.fetch_polygon(ticker, polygon_api_key))
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []
        for article in all_news:
            title = article.get('title', '').lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(article)
        
        # Sort by date (most recent first)
        unique_news.sort(
            key=lambda x: x.get('published_at', ''),
            reverse=True
        )
        
        return unique_news[:20]  # Return top 20


def get_comprehensive_news(
    ticker: str,
    news_api_key: str = None,
    finnhub_api_key: str = None,
    polygon_api_key: str = None,
    days: int = 7
) -> List[Dict]:
    """
    Get comprehensive news from multiple sources.
    
    Args:
        ticker: Stock ticker symbol
        news_api_key: NewsAPI key
        finnhub_api_key: Finnhub key
        polygon_api_key: Polygon key
        days: Lookback period in days
        
    Returns:
        List of news articles
    """
    aggregator = NewsAggregator(news_api_key, finnhub_api_key)
    return aggregator.aggregate_all(ticker, days, polygon_api_key)

