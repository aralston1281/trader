"""
Ranking and scoring logic for combining signals.
"""
import logging
from typing import List, Optional
from ..models import Fundamentals, OptionsSnapshot, Catalyst, SignalBundle, RankedIdea
from ..signals import fundamental_bias, premium_bias, catalyst_score
from ..strategy import pick_strategy
from ..config import Settings

logger = logging.getLogger(__name__)


def calculate_overall_score(
    signals: SignalBundle,
    opts: OptionsSnapshot,
    fund: Fundamentals
) -> float:
    """
    Calculate overall score from signal bundle.
    
    Uses weighted combination:
    - Fundamental bias: 60%
    - Premium bias: 25%
    - Catalyst: 15%
    
    Applies penalties for low liquidity or small market cap.
    
    Args:
        signals: SignalBundle with all signal scores
        opts: OptionsSnapshot for liquidity
        fund: Fundamentals for market cap
        
    Returns:
        Overall score from 0 to 10
    """
    # Normalize fundamental bias from -10/10 to 0/10 scale
    # We care about conviction, not direction
    fund_magnitude = abs(signals.fund_bias)
    
    # Normalize premium bias to 0/10 (absolute value represents strength)
    premium_magnitude = abs(signals.premium_bias)
    
    # Catalyst is already 0-10
    catalyst_val = signals.catalyst_score
    
    # Weighted combination
    base_score = (
        fund_magnitude * Settings.WEIGHT_FUNDAMENTAL +
        premium_magnitude * Settings.WEIGHT_PREMIUM +
        catalyst_val * Settings.WEIGHT_CATALYST
    )
    
    # Apply liquidity penalty
    liquidity_penalty = 0.0
    if opts.liquidity_score < Settings.MIN_LIQUIDITY_SCORE:
        liquidity_penalty = (Settings.MIN_LIQUIDITY_SCORE - opts.liquidity_score) * 0.5
    
    # Apply market cap penalty for very small caps
    mcap_penalty = 0.0
    if fund.market_cap < Settings.MIN_MARKET_CAP:
        mcap_penalty = 1.0
    
    final_score = base_score - liquidity_penalty - mcap_penalty
    
    # Clamp to 0-10
    final_score = max(0.0, min(10.0, final_score))
    
    return final_score


def rank_candidates(
    tickers: List[str],
    fundamentals: dict[str, Fundamentals],
    options: dict[str, OptionsSnapshot],
    catalysts: dict[str, Catalyst]
) -> List[RankedIdea]:
    """
    Rank all candidate tickers and return sorted list of ideas.
    
    Args:
        tickers: List of ticker symbols
        fundamentals: Dict mapping ticker to Fundamentals
        options: Dict mapping ticker to OptionsSnapshot
        catalysts: Dict mapping ticker to Catalyst
        
    Returns:
        Sorted list of RankedIdea objects (best first)
    """
    ideas = []
    
    for ticker in tickers:
        fund = fundamentals.get(ticker)
        opts = options.get(ticker)
        cat = catalysts.get(ticker)
        
        # Skip if missing critical data
        if not fund or not opts or not cat:
            logger.warning(f"Skipping {ticker} - missing data")
            continue
        
        # Calculate signals
        try:
            fund_bias_score = fundamental_bias(fund)
            prem_bias_score = premium_bias(opts)
            cat_score = catalyst_score(cat)
            
            signals = SignalBundle(
                ticker=ticker,
                fund_bias=fund_bias_score,
                premium_bias=prem_bias_score,
                catalyst_score=cat_score
            )
            
            # Calculate overall score
            overall_score = calculate_overall_score(signals, opts, fund)
            
            # Pick strategy
            strategy, notes = pick_strategy(signals, opts)
            
            # Create ranked idea
            idea = RankedIdea(
                ticker=ticker,
                score=overall_score,
                signals=signals,
                options=opts,
                fundamentals=fund,
                catalyst=cat,
                strategy=strategy,
                notes=notes
            )
            
            ideas.append(idea)
            
        except Exception as e:
            logger.error(f"Error ranking {ticker}: {e}")
            continue
    
    # Sort by score (descending)
    ideas.sort(key=lambda x: x.score, reverse=True)
    
    # Limit to MAX_PICKS
    ideas = ideas[:Settings.MAX_PICKS]
    
    logger.info(f"Ranked {len(ideas)} ideas")
    return ideas

