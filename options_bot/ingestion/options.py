"""
Options data ingestion and analysis.
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Optional
from datetime import datetime, timedelta
import logging

from ..models import OptionsSnapshot

logger = logging.getLogger(__name__)


def calculate_hv(prices: pd.Series, window: int = 30) -> float:
    """
    Calculate historical volatility (annualized).
    
    Args:
        prices: Series of closing prices
        window: Rolling window for calculation
        
    Returns:
        Annualized historical volatility
    """
    returns = np.log(prices / prices.shift(1))
    volatility = returns.rolling(window=window).std() * np.sqrt(252)
    return volatility.iloc[-1] if not pd.isna(volatility.iloc[-1]) else None


def calculate_iv_rank(iv_history: pd.Series, current_iv: float) -> float:
    """
    Calculate IV rank (percentile over period).
    
    Args:
        iv_history: Historical IV values
        current_iv: Current IV value
        
    Returns:
        IV rank (0-100)
    """
    if len(iv_history) < 2:
        return 50.0  # Default to mid-range
    
    percentile = (iv_history < current_iv).sum() / len(iv_history) * 100
    return percentile


def score_liquidity(volume: int, open_interest: int) -> float:
    """
    Score options liquidity (0-10 scale).
    
    Args:
        volume: Option volume
        open_interest: Open interest
        
    Returns:
        Liquidity score 0-10
    """
    # Simple heuristic - can be refined
    combined = volume + (open_interest * 0.5)
    
    if combined > 10000:
        return 10.0
    elif combined > 5000:
        return 8.0
    elif combined > 1000:
        return 6.0
    elif combined > 500:
        return 4.0
    elif combined > 100:
        return 2.0
    else:
        return 1.0


def get_options_snapshot(ticker: str) -> Optional[OptionsSnapshot]:
    """
    Fetch options structure data for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        OptionsSnapshot object or None if data unavailable
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get current price
        current_price = stock.info.get('currentPrice') or stock.info.get('regularMarketPrice')
        if not current_price:
            logger.warning(f"No current price for {ticker}")
            return None
        
        # Calculate historical volatility
        hist = stock.history(period="3mo")
        if hist.empty:
            logger.warning(f"No price history for {ticker}")
            return None
            
        hv30 = calculate_hv(hist['Close'], window=30)
        
        # Get options chain
        try:
            expiration_dates = stock.options
            if not expiration_dates:
                logger.warning(f"No options available for {ticker}")
                return None
            
            # Find expiration closest to 35 DTE
            target_date = datetime.now() + timedelta(days=35)
            closest_exp = min(
                expiration_dates,
                key=lambda x: abs((datetime.strptime(x, '%Y-%m-%d') - target_date).days)
            )
            
            opt_chain = stock.option_chain(closest_exp)
            calls = opt_chain.calls
            puts = opt_chain.puts
            
            # Find ATM options
            calls['dist'] = abs(calls['strike'] - current_price)
            puts['dist'] = abs(puts['strike'] - current_price)
            
            atm_call = calls.loc[calls['dist'].idxmin()]
            atm_put = puts.loc[puts['dist'].idxmin()]
            
            # ATM IV (average of call and put)
            atm_iv = None
            if 'impliedVolatility' in atm_call and 'impliedVolatility' in atm_put:
                call_iv = atm_call['impliedVolatility']
                put_iv = atm_put['impliedVolatility']
                if call_iv > 0 and put_iv > 0:
                    atm_iv = (call_iv + put_iv) / 2
            
            # Calculate IV rank (simplified - using current vs HV as proxy)
            iv_rank = 50.0  # Default
            if atm_iv and hv30:
                if atm_iv > hv30:
                    iv_rank = 60.0 + min((atm_iv / hv30 - 1) * 100, 40.0)
                else:
                    iv_rank = 60.0 - min((1 - atm_iv / hv30) * 100, 60.0)
            
            # Skew calculation (25-delta risk reversal approximation)
            # Use 25% OTM options as proxy
            otm_strike_call = current_price * 1.05
            otm_strike_put = current_price * 0.95
            
            calls_otm = calls[calls['strike'] >= otm_strike_call]
            puts_otm = puts[puts['strike'] <= otm_strike_put]
            
            skew = None
            if not calls_otm.empty and not puts_otm.empty:
                otm_call = calls_otm.iloc[0]
                otm_put = puts_otm.iloc[-1]
                if 'impliedVolatility' in otm_call and 'impliedVolatility' in otm_put:
                    put_iv_otm = otm_put['impliedVolatility']
                    call_iv_otm = otm_call['impliedVolatility']
                    if put_iv_otm > 0 and call_iv_otm > 0:
                        skew = put_iv_otm - call_iv_otm  # Positive = put skew
            
            # Liquidity scoring
            call_liq = score_liquidity(
                calls['volume'].sum(),
                calls['openInterest'].sum()
            )
            put_liq = score_liquidity(
                puts['volume'].sum(),
                puts['openInterest'].sum()
            )
            
            # Term structure slope (simplified - would need multiple expirations)
            term_slope = None  # Placeholder for now
            
            snapshot = OptionsSnapshot(
                ticker=ticker,
                spot_price=current_price,
                hv30=hv30,
                atm_iv_dte35=atm_iv,
                iv_rank_1y=iv_rank,
                skew_25d_rr=skew,
                term_slope_iv=term_slope,
                liq_calls_score=call_liq,
                liq_puts_score=put_liq,
                avg_option_volume=int(calls['volume'].sum() + puts['volume'].sum()),
                open_interest=int(calls['openInterest'].sum() + puts['openInterest'].sum())
            )
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Error processing options chain for {ticker}: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching options data for {ticker}: {e}")
        return None

