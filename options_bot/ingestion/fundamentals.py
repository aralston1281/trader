"""
Fundamental data ingestion using yfinance.
"""
import yfinance as yf
from typing import Optional
import logging

from ..models import Fundamentals

logger = logging.getLogger(__name__)


def get_fundamentals(ticker: str) -> Optional[Fundamentals]:
    """
    Fetch fundamental data for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Fundamentals object or None if data unavailable
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract fundamental metrics
        fundamentals = Fundamentals(
            ticker=ticker,
            market_cap=info.get('marketCap', 0),
            pe_ratio=info.get('trailingPE'),
            forward_pe=info.get('forwardPE'),
            profit_margins=info.get('profitMargins'),
            debt_to_equity=info.get('debtToEquity'),
            sector=info.get('sector'),
            revenue_growth=info.get('revenueGrowth'),
            earnings_growth=info.get('earningsGrowth')
        )
        
        return fundamentals
        
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {ticker}: {e}")
        return None


def get_price_history(ticker: str, period: str = "1y") -> Optional[any]:
    """
    Fetch price history for volatility calculations.
    
    Args:
        ticker: Stock ticker symbol
        period: Period for historical data (default: 1y)
        
    Returns:
        DataFrame with price history or None
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
        
    except Exception as e:
        logger.error(f"Error fetching price history for {ticker}: {e}")
        return None

