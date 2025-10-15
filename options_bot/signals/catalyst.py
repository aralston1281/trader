"""
Catalyst scoring.
"""
import logging
from ..models import Catalyst

logger = logging.getLogger(__name__)


def catalyst_score(cat: Catalyst) -> float:
    """
    Calculate catalyst score.
    
    Returns a score from 0 (no catalysts) to 10 (strong catalysts)
    based on upcoming events and news.
    
    Factors:
    - Earnings proximity (±5 days)
    - News sentiment
    - Major events
    
    Args:
        cat: Catalyst object
        
    Returns:
        Catalyst score from 0 to 10
    """
    score = 0.0
    
    # Earnings proximity
    if cat.days_to_earnings is not None:
        days_abs = abs(cat.days_to_earnings)
        
        if days_abs <= 2:
            score += 5.0  # Very near earnings
        elif days_abs <= 5:
            score += 3.0  # Near earnings
        elif days_abs <= 10:
            score += 1.5  # Approaching earnings
        elif days_abs <= 20:
            score += 0.5  # Earnings on horizon
    
    # Major events
    if cat.has_major_event_7d:
        score += 2.0
    
    # Sentiment from headlines
    if cat.sentiment_score is not None:
        # Positive or negative sentiment adds to catalyst score
        # (direction handled separately by fundamental bias)
        sentiment_magnitude = abs(cat.sentiment_score)
        if sentiment_magnitude > 0.5:
            score += 2.0  # Strong sentiment
        elif sentiment_magnitude > 0.3:
            score += 1.0  # Moderate sentiment
    
    # News volume (more headlines = more attention)
    if cat.headlines:
        headline_count = len(cat.headlines)
        if headline_count >= 5:
            score += 1.5
        elif headline_count >= 3:
            score += 1.0
        elif headline_count >= 1:
            score += 0.5
    
    # Clamp score to 0 to 10 range
    score = max(0.0, min(10.0, score))
    
    logger.debug(f"Catalyst score for {cat.ticker}: {score:.2f} (Days to earnings: {cat.days_to_earnings})")
    return score

