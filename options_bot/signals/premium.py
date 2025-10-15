"""
Premium structure bias scoring.
"""
import logging
from ..models import OptionsSnapshot

logger = logging.getLogger(__name__)


def premium_bias(opts: OptionsSnapshot) -> float:
    """
    Calculate premium structure bias score.
    
    Returns a score from -10 (very low premium) to +10 (very high premium)
    based on options structure metrics.
    
    High premium (positive score) suggests:
    - Good for selling premium strategies
    - High IV relative to HV
    - High IV rank
    
    Low premium (negative score) suggests:
    - Good for buying options
    - Low IV relative to HV
    - Low IV rank
    
    Args:
        opts: OptionsSnapshot object
        
    Returns:
        Premium bias score from -10 to 10
    """
    score = 0.0
    
    # IV/HV ratio (most important factor)
    iv_hv = opts.iv_hv_ratio
    if iv_hv is not None:
        if iv_hv > 1.5:
            score += 4.0  # Very high premium
        elif iv_hv > 1.2:
            score += 2.5  # High premium
        elif iv_hv > 1.0:
            score += 1.0  # Elevated premium
        elif iv_hv < 0.7:
            score -= 4.0  # Very low premium
        elif iv_hv < 0.85:
            score -= 2.5  # Low premium
        elif iv_hv < 1.0:
            score -= 1.0  # Below average premium
    
    # IV Rank
    if opts.iv_rank_1y is not None:
        if opts.iv_rank_1y > 80:
            score += 3.0  # Very high IV rank
        elif opts.iv_rank_1y > 60:
            score += 1.5  # High IV rank
        elif opts.iv_rank_1y < 20:
            score -= 3.0  # Very low IV rank
        elif opts.iv_rank_1y < 40:
            score -= 1.5  # Low IV rank
    
    # Skew (put/call skew)
    if opts.skew_25d_rr is not None:
        # Positive skew = puts more expensive (fear)
        if opts.skew_25d_rr > 0.05:
            score += 1.0  # Put skew suggests premium in puts
        elif opts.skew_25d_rr < -0.05:
            score -= 0.5  # Call skew (unusual, slightly negative)
    
    # Term structure slope
    if opts.term_slope_iv is not None:
        # Positive slope = front month cheap (contango)
        # Negative slope = front month expensive (backwardation)
        if opts.term_slope_iv > 0.05:
            score -= 1.0  # Front month relatively cheap
        elif opts.term_slope_iv < -0.05:
            score += 1.0  # Front month relatively expensive
    
    # Clamp score to -10 to 10 range
    score = max(-10.0, min(10.0, score))
    
    logger.debug(f"Premium bias for {opts.ticker}: {score:.2f} (IV/HV: {iv_hv}, IVR: {opts.iv_rank_1y})")
    return score

