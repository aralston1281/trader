"""
Options strategy picker based on signals and market conditions.
"""
import logging
from ..models import SignalBundle, OptionsSnapshot

logger = logging.getLogger(__name__)


def pick_strategy(signals: SignalBundle, opts: OptionsSnapshot) -> tuple[str, str]:
    """
    Select appropriate options strategy based on signals and premium structure.
    
    Strategy Selection Logic:
    - High IV + Bullish → Bull Put Spread, Covered Call
    - Low IV + Bullish → Long Call, Call Debit Spread
    - High IV + Bearish → Bear Call Spread, Long Put (sell after)
    - Low IV + Bearish → Long Put, Put Debit Spread
    - Neutral + High IV → Iron Condor, Short Straddle/Strangle
    - Neutral + Low IV → Long Straddle, Calendar Spread
    
    Args:
        signals: SignalBundle with bias scores
        opts: OptionsSnapshot with premium information
        
    Returns:
        Tuple of (strategy_name, notes)
    """
    
    # Determine directional bias
    fund_bias = signals.fund_bias
    is_bullish = fund_bias > 2
    is_bearish = fund_bias < -2
    is_neutral = not is_bullish and not is_bearish
    
    # Determine premium level
    premium_bias = signals.premium_bias
    is_high_premium = premium_bias > 2
    is_low_premium = premium_bias < -2
    is_moderate_premium = not is_high_premium and not is_low_premium
    
    # Get IV/HV ratio for additional context
    iv_hv = opts.iv_hv_ratio or 1.0
    
    # Strategy selection
    strategy = "UNDEFINED"
    notes = ""
    
    # BULLISH scenarios
    if is_bullish:
        if is_high_premium:
            strategy = "BULL PUT SPREAD"
            notes = f"Bullish bias with high premium (IV/HV: {iv_hv:.2f}). Sell put spread to collect premium."
        elif is_low_premium:
            strategy = "LONG CALL"
            notes = f"Bullish bias with cheap options (IV/HV: {iv_hv:.2f}). Buy calls outright."
        else:
            strategy = "CALL DEBIT SPREAD"
            notes = f"Bullish bias with moderate premium (IV/HV: {iv_hv:.2f}). Call spread for defined risk."
    
    # BEARISH scenarios
    elif is_bearish:
        if is_high_premium:
            strategy = "BEAR CALL SPREAD"
            notes = f"Bearish bias with high premium (IV/HV: {iv_hv:.2f}). Sell call spread to collect premium."
        elif is_low_premium:
            strategy = "LONG PUT"
            notes = f"Bearish bias with cheap options (IV/HV: {iv_hv:.2f}). Buy puts outright."
        else:
            strategy = "PUT DEBIT SPREAD"
            notes = f"Bearish bias with moderate premium (IV/HV: {iv_hv:.2f}). Put spread for defined risk."
    
    # NEUTRAL scenarios
    else:
        if is_high_premium:
            if signals.catalyst_score > 5:
                # High catalyst + high IV = potential for big move
                strategy = "IRON CONDOR"
                notes = f"Neutral with high IV (IV/HV: {iv_hv:.2f}) and catalyst. Iron condor for range-bound profit."
            else:
                strategy = "SHORT STRANGLE"
                notes = f"Neutral with high IV (IV/HV: {iv_hv:.2f}). Sell strangle to collect premium."
        elif is_low_premium:
            if signals.catalyst_score > 5:
                # Catalyst coming + cheap options = potential volatility expansion
                strategy = "LONG STRADDLE"
                notes = f"Neutral with cheap options (IV/HV: {iv_hv:.2f}) and catalyst. Buy straddle for volatility play."
            else:
                strategy = "CALENDAR SPREAD"
                notes = f"Neutral with low IV (IV/HV: {iv_hv:.2f}). Calendar spread to capture theta."
        else:
            strategy = "IRON CONDOR"
            notes = f"Neutral outlook with moderate premium (IV/HV: {iv_hv:.2f}). Iron condor for range-bound profit."
    
    # Add catalyst note if significant
    if signals.catalyst_score > 5:
        catalyst_note = f" Catalyst score: {signals.catalyst_score:.1f}/10."
        notes += catalyst_note
    
    # Add liquidity warning if needed
    if opts.liquidity_score < 5:
        notes += f" ⚠️ Lower liquidity (score: {opts.liquidity_score:.1f}/10)."
    
    logger.debug(f"Strategy for {signals.ticker}: {strategy}")
    return strategy, notes

