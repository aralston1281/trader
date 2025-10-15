"""
Stock splits and corporate actions tracker.
"""
import yfinance as yf
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def get_split_history(ticker: str) -> List[Dict]:
    """
    Get historical stock splits.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        List of split events
    """
    try:
        stock = yf.Ticker(ticker)
        splits = stock.splits
        
        if splits.empty:
            return []
        
        split_events = []
        for date, ratio in splits.items():
            split_events.append({
                'date': date.strftime('%Y-%m-%d'),
                'ratio': float(ratio),
                'description': f"{int(ratio)}:1 split" if ratio > 1 else f"1:{int(1/ratio)} reverse split"
            })
        
        return split_events
        
    except Exception as e:
        logger.error(f"Error fetching split history for {ticker}: {e}")
        return []


def get_dividend_history(ticker: str, years: int = 1) -> List[Dict]:
    """
    Get dividend history.
    
    Args:
        ticker: Stock ticker symbol
        years: Lookback period in years
        
    Returns:
        List of dividend events
    """
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        
        if dividends.empty:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=365 * years)
        recent_divs = dividends[dividends.index > cutoff_date]
        
        div_events = []
        for date, amount in recent_divs.items():
            div_events.append({
                'date': date.strftime('%Y-%m-%d'),
                'amount': float(amount)
            })
        
        return div_events
        
    except Exception as e:
        logger.error(f"Error fetching dividend history for {ticker}: {e}")
        return []


def predict_split_likelihood(ticker: str, current_price: float) -> Dict[str, any]:
    """
    Predict likelihood of upcoming stock split based on patterns.
    
    Args:
        ticker: Stock ticker symbol
        current_price: Current stock price
        
    Returns:
        Dictionary with split prediction
    """
    try:
        # Common patterns for splits:
        # 1. Stock trading at high prices (>$500 for big tech)
        # 2. Historical pattern of splitting
        # 3. Company announcements
        
        split_history = get_split_history(ticker)
        
        # Check if company has split history
        has_split_before = len(split_history) > 0
        
        # Check recent splits (within last 5 years)
        recent_splits = [s for s in split_history 
                        if (datetime.now() - datetime.strptime(s['date'], '%Y-%m-%d')).days < 1825]
        
        # Price-based likelihood
        price_likelihood = 0.0
        price_note = ""
        
        if current_price > 1000:
            price_likelihood = 0.8
            price_note = "Very high price, split likely"
        elif current_price > 500:
            price_likelihood = 0.6
            price_note = "High price, split possible"
        elif current_price > 300:
            price_likelihood = 0.3
            price_note = "Moderately high price"
        elif current_price < 10 and has_split_before:
            price_likelihood = 0.4
            price_note = "Low price, reverse split possible"
        else:
            price_note = "Price in normal range"
        
        # Historical pattern boost
        if len(recent_splits) > 0:
            price_likelihood = min(price_likelihood * 1.5, 1.0)
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'split_likelihood': price_likelihood,
            'has_split_history': has_split_before,
            'recent_splits_count': len(recent_splits),
            'last_split': split_history[-1] if split_history else None,
            'note': price_note,
            'catalyst_score': price_likelihood * 5  # 0-5 score
        }
        
    except Exception as e:
        logger.error(f"Error predicting split for {ticker}: {e}")
        return {
            'ticker': ticker,
            'split_likelihood': 0.0,
            'has_split_history': False,
            'note': 'Unable to analyze',
            'catalyst_score': 0
        }


def get_corporate_actions(ticker: str) -> Dict[str, any]:
    """
    Get comprehensive corporate actions information.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with corporate actions
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        # Get splits
        splits = get_split_history(ticker)
        
        # Get dividends
        dividends = get_dividend_history(ticker, years=1)
        
        # Predict split
        split_prediction = predict_split_likelihood(ticker, current_price)
        
        # Check for special dividends or buybacks
        has_dividend = len(dividends) > 0
        dividend_yield = info.get('dividendYield', 0)
        
        # Calculate catalyst score
        catalyst_score = 0
        notes = []
        
        if split_prediction['split_likelihood'] > 0.6:
            catalyst_score += 4
            notes.append(f"High split likelihood: {split_prediction['note']}")
        
        if splits and (datetime.now() - datetime.strptime(splits[-1]['date'], '%Y-%m-%d')).days < 180:
            catalyst_score += 3
            notes.append(f"Recent split: {splits[-1]['description']}")
        
        if dividend_yield and dividend_yield > 0.05:
            catalyst_score += 2
            notes.append(f"High dividend yield: {dividend_yield*100:.1f}%")
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'splits': splits,
            'recent_dividends': dividends,
            'split_prediction': split_prediction,
            'has_dividend': has_dividend,
            'dividend_yield': dividend_yield,
            'catalyst_score': min(catalyst_score, 10),
            'notes': '; '.join(notes) if notes else 'No significant corporate actions'
        }
        
    except Exception as e:
        logger.error(f"Error fetching corporate actions for {ticker}: {e}")
        return {
            'ticker': ticker,
            'catalyst_score': 0,
            'notes': 'Unable to fetch corporate actions'
        }

