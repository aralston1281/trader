"""
Catalyst data ingestion (earnings, news, events).
"""
import yfinance as yf
import feedparser
import requests
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from ..models import Catalyst
from ..config import Settings

logger = logging.getLogger(__name__)


def get_earnings_date(ticker: str) -> tuple[Optional[datetime], Optional[str]]:
    """
    Get next earnings date and timing (BMO/AMC).
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Tuple of (earnings_date, timing)
    """
    try:
        stock = yf.Ticker(ticker)
        calendar = stock.calendar
        
        if calendar is not None and 'Earnings Date' in calendar:
            earnings_info = calendar['Earnings Date']
            if isinstance(earnings_info, (list, tuple)) and len(earnings_info) > 0:
                earnings_date = earnings_info[0]
                if isinstance(earnings_date, str):
                    earnings_date = datetime.strptime(earnings_date, '%Y-%m-%d')
                
                # Timing is not always available from yfinance, default to unknown
                timing = None  # Could be enhanced with additional data sources
                
                return earnings_date, timing
        
        return None, None
        
    except Exception as e:
        logger.debug(f"Error fetching earnings for {ticker}: {e}")
        return None, None


def get_news_headlines(ticker: str, max_headlines: int = 5) -> List[str]:
    """
    Fetch recent news headlines for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        max_headlines: Maximum number of headlines to return
        
    Returns:
        List of headline strings
    """
    headlines = []
    
    try:
        # Try yfinance news first
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if news:
            for item in news[:max_headlines]:
                title = item.get('title', '')
                if title:
                    headlines.append(title)
    
    except Exception as e:
        logger.debug(f"Error fetching news for {ticker}: {e}")
    
    # Could add additional news sources here (RSS feeds, news APIs, etc.)
    
    return headlines


def analyze_sentiment(headlines: List[str]) -> Optional[float]:
    """
    Analyze sentiment of headlines.
    
    Args:
        headlines: List of headline strings
        
    Returns:
        Sentiment score -1 (bearish) to 1 (bullish) or None
    """
    if not headlines or not Settings.USE_FINBERT:
        return None
    
    try:
        # Placeholder for FinBERT sentiment analysis
        # This would require the transformers library and FinBERT model
        # For now, return None
        # 
        # from transformers import pipeline
        # sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        # results = sentiment_analyzer(headlines)
        # scores = [r['score'] if r['label'] == 'positive' else -r['score'] for r in results]
        # return sum(scores) / len(scores)
        
        return None
        
    except Exception as e:
        logger.debug(f"Error analyzing sentiment: {e}")
        return None


def get_catalyst(ticker: str) -> Optional[Catalyst]:
    """
    Fetch catalyst information for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Catalyst object or None if error
    """
    try:
        # Get earnings date
        earnings_date, timing = get_earnings_date(ticker)
        
        # Calculate days to earnings
        days_to_earnings = None
        if earnings_date:
            # Convert earnings_date to datetime if it's a date object
            if hasattr(earnings_date, 'date'):
                # It's already a datetime
                days_to_earnings = (earnings_date - datetime.now()).days
            else:
                # It's a date, convert to datetime
                earnings_datetime = datetime.combine(earnings_date, datetime.min.time())
                days_to_earnings = (earnings_datetime - datetime.now()).days
        
        # Get news headlines
        headlines = get_news_headlines(ticker)
        
        # Analyze sentiment
        sentiment = analyze_sentiment(headlines)
        
        # Check for major events in next 7 days
        has_major_event = False
        event_description = None
        
        if days_to_earnings is not None and abs(days_to_earnings) <= 7:
            has_major_event = True
            event_description = f"Earnings in {days_to_earnings} days"
        
        catalyst = Catalyst(
            ticker=ticker,
            next_earnings_date=earnings_date,
            earnings_bmo_amc=timing,
            headlines=headlines,
            sentiment_score=sentiment,
            has_major_event_7d=has_major_event,
            event_description=event_description,
            days_to_earnings=days_to_earnings
        )
        
        return catalyst
        
    except Exception as e:
        logger.error(f"Error fetching catalysts for {ticker}: {e}")
        return None

