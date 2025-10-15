"""
Technical analysis signal generation.
"""
import logging
from typing import Dict, Optional
from ..ingestion.technical_analysis import get_technical_analysis

logger = logging.getLogger(__name__)


def technical_bias(ticker: str, ta_data: Dict = None) -> float:
    """
    Calculate technical analysis bias score.
    
    Returns a score from -10 (very bearish) to +10 (very bullish)
    based on technical indicators.
    
    Factors:
    - RSI (overbought/oversold)
    - MACD (trend direction)
    - Moving averages (trend confirmation)
    - Support/Resistance (price action)
    - Volume (confirmation)
    - Trend strength (ADX)
    
    Args:
        ticker: Stock ticker symbol
        ta_data: Optional pre-calculated technical analysis data
        
    Returns:
        Bias score from -10 to 10
    """
    try:
        # Get technical analysis if not provided
        if ta_data is None:
            ta_data = get_technical_analysis(ticker)
        
        if not ta_data or 'bias_score' not in ta_data:
            logger.warning(f"No technical data available for {ticker}")
            return 0.0
        
        # Technical analysis module already provides a -10 to +10 bias score
        # We can return it directly or add additional logic
        base_score = ta_data.get('bias_score', 0.0)
        
        # Additional adjustments based on specific indicators
        adjustments = 0.0
        
        # RSI extremes
        rsi = ta_data.get('rsi', 50)
        if rsi < 25:  # Very oversold
            adjustments += 2.0
        elif rsi > 75:  # Very overbought
            adjustments -= 2.0
        
        # Trend strength
        trend = ta_data.get('trend', {})
        if trend.get('trending') and trend.get('adx', 0) > 40:
            # Strong trend - boost the signal
            if base_score > 0:
                adjustments += 1.0
            elif base_score < 0:
                adjustments -= 1.0
        
        # Volume confirmation
        volume = ta_data.get('volume', {})
        if volume.get('high_volume') and volume.get('obv_bullish'):
            if base_score > 0:
                adjustments += 0.5
        elif volume.get('high_volume') and not volume.get('obv_bullish'):
            if base_score < 0:
                adjustments -= 0.5
        
        # Support/Resistance proximity
        sr = ta_data.get('support_resistance', {})
        nearest_support = sr.get('nearest_support')
        nearest_resistance = sr.get('nearest_resistance')
        
        if nearest_support or nearest_resistance:
            # Near support = potential bounce
            # Near resistance = potential rejection
            # (This is a simple heuristic, could be enhanced)
            pass
        
        final_score = base_score + adjustments
        
        # Clamp to -10 to 10 range
        final_score = max(-10.0, min(10.0, final_score))
        
        logger.debug(f"Technical bias for {ticker}: {final_score:.2f}")
        return final_score
        
    except Exception as e:
        logger.error(f"Error calculating technical bias for {ticker}: {e}")
        return 0.0


def get_technical_summary_text(ticker: str, ta_data: Dict = None) -> str:
    """
    Generate human-readable technical analysis summary.
    
    Args:
        ticker: Stock ticker symbol
        ta_data: Optional pre-calculated technical analysis data
        
    Returns:
        Summary string
    """
    try:
        if ta_data is None:
            ta_data = get_technical_analysis(ticker)
        
        if not ta_data:
            return "Technical data unavailable"
        
        summary_parts = []
        
        # RSI
        rsi = ta_data.get('rsi')
        if rsi:
            if rsi < 30:
                summary_parts.append(f"RSI oversold ({rsi:.0f})")
            elif rsi > 70:
                summary_parts.append(f"RSI overbought ({rsi:.0f})")
            else:
                summary_parts.append(f"RSI neutral ({rsi:.0f})")
        
        # MACD
        macd = ta_data.get('macd', {})
        if macd.get('bullish'):
            summary_parts.append("MACD bullish")
        else:
            summary_parts.append("MACD bearish")
        
        # Moving averages
        mas = ta_data.get('moving_averages', {})
        if mas.get('golden_cross'):
            summary_parts.append("Golden cross")
        elif mas.get('death_cross'):
            summary_parts.append("Death cross")
        elif mas.get('above_sma_200'):
            summary_parts.append("Above 200 SMA")
        else:
            summary_parts.append("Below 200 SMA")
        
        # Trend
        trend = ta_data.get('trend', {})
        if trend.get('trending'):
            summary_parts.append(f"{trend.get('strength', 'Moderate')} trend")
        
        return "; ".join(summary_parts)
        
    except Exception as e:
        logger.error(f"Error generating technical summary for {ticker}: {e}")
        return "Technical summary unavailable"

