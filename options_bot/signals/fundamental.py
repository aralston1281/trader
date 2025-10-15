"""
Fundamental bias scoring.
"""
import logging
from ..models import Fundamentals

logger = logging.getLogger(__name__)


def fundamental_bias(fund: Fundamentals) -> float:
    """
    Calculate fundamental bias score.
    
    Returns a score from -10 (very bearish) to +10 (very bullish)
    based on fundamental metrics.
    
    Factors:
    - Lower P/E ratio → bullish
    - Higher profit margins → bullish
    - Lower debt-to-equity → bullish
    - Revenue/earnings growth → bullish
    
    Args:
        fund: Fundamentals object
        
    Returns:
        Bias score from -10 to 10
    """
    score = 0.0
    
    # P/E ratio scoring
    if fund.pe_ratio is not None and fund.pe_ratio > 0:
        if fund.pe_ratio < 15:
            score += 3.0  # Very cheap
        elif fund.pe_ratio < 25:
            score += 1.0  # Reasonable
        elif fund.pe_ratio > 40:
            score -= 2.0  # Expensive
        elif fund.pe_ratio > 60:
            score -= 4.0  # Very expensive
    
    # Forward P/E (if available, weight more heavily)
    if fund.forward_pe is not None and fund.forward_pe > 0:
        if fund.forward_pe < 15:
            score += 2.0
        elif fund.forward_pe < 20:
            score += 1.0
        elif fund.forward_pe > 35:
            score -= 2.0
    
    # Profit margins
    if fund.profit_margins is not None:
        if fund.profit_margins > 0.20:  # 20%+ margins
            score += 2.0
        elif fund.profit_margins > 0.10:  # 10%+ margins
            score += 1.0
        elif fund.profit_margins < 0:  # Negative margins
            score -= 3.0
        elif fund.profit_margins < 0.05:  # <5% margins
            score -= 1.0
    
    # Debt-to-equity ratio
    if fund.debt_to_equity is not None:
        if fund.debt_to_equity < 0.3:
            score += 1.5  # Low debt
        elif fund.debt_to_equity < 0.5:
            score += 0.5  # Reasonable debt
        elif fund.debt_to_equity > 2.0:
            score -= 2.0  # High debt
        elif fund.debt_to_equity > 3.0:
            score -= 3.0  # Very high debt
    
    # Revenue growth
    if fund.revenue_growth is not None:
        if fund.revenue_growth > 0.20:  # 20%+ growth
            score += 2.0
        elif fund.revenue_growth > 0.10:  # 10%+ growth
            score += 1.0
        elif fund.revenue_growth < -0.10:  # Declining revenue
            score -= 2.0
    
    # Earnings growth
    if fund.earnings_growth is not None:
        if fund.earnings_growth > 0.25:  # 25%+ growth
            score += 1.5
        elif fund.earnings_growth > 0.15:  # 15%+ growth
            score += 0.5
        elif fund.earnings_growth < -0.15:  # Declining earnings
            score -= 1.5
    
    # Clamp score to -10 to 10 range
    score = max(-10.0, min(10.0, score))
    
    logger.debug(f"Fundamental bias for {fund.ticker}: {score:.2f}")
    return score

