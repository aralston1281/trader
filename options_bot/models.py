"""
Data models for the options bot framework.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Fundamentals:
    """Fundamental data for a ticker."""
    ticker: str
    market_cap: float
    pe_ratio: Optional[float]
    forward_pe: Optional[float]
    profit_margins: Optional[float]
    debt_to_equity: Optional[float]
    sector: Optional[str]
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'ticker': self.ticker,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'forward_pe': self.forward_pe,
            'profit_margins': self.profit_margins,
            'debt_to_equity': self.debt_to_equity,
            'sector': self.sector,
            'revenue_growth': self.revenue_growth,
            'earnings_growth': self.earnings_growth
        }


@dataclass
class OptionsSnapshot:
    """Options structure data for a ticker."""
    ticker: str
    spot_price: float
    hv30: Optional[float]  # 30-day historical volatility
    atm_iv_dte35: Optional[float]  # ATM IV for ~35 DTE
    iv_rank_1y: Optional[float]  # IV rank over 1 year (0-100)
    skew_25d_rr: Optional[float]  # 25-delta risk reversal (put-call skew)
    term_slope_iv: Optional[float]  # IV term structure slope
    liq_calls_score: float = 0.0  # Liquidity score for calls (0-10)
    liq_puts_score: float = 0.0  # Liquidity score for puts (0-10)
    avg_option_volume: Optional[int] = None
    open_interest: Optional[int] = None
    
    @property
    def liquidity_score(self) -> float:
        """Average liquidity score across calls and puts."""
        return (self.liq_calls_score + self.liq_puts_score) / 2
    
    @property
    def iv_hv_ratio(self) -> Optional[float]:
        """Calculate IV/HV ratio if both available."""
        if self.atm_iv_dte35 and self.hv30 and self.hv30 > 0:
            return self.atm_iv_dte35 / self.hv30
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'ticker': self.ticker,
            'spot_price': self.spot_price,
            'hv30': self.hv30,
            'atm_iv_dte35': self.atm_iv_dte35,
            'iv_rank_1y': self.iv_rank_1y,
            'skew_25d_rr': self.skew_25d_rr,
            'term_slope_iv': self.term_slope_iv,
            'liq_calls_score': self.liq_calls_score,
            'liq_puts_score': self.liq_puts_score,
            'liquidity_score': self.liquidity_score,
            'iv_hv_ratio': self.iv_hv_ratio
        }


@dataclass
class Catalyst:
    """Catalyst information for a ticker."""
    ticker: str
    next_earnings_date: Optional[datetime]
    earnings_bmo_amc: Optional[str]  # "BMO" (before market open) or "AMC" (after market close)
    headlines: list[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None  # -1 to 1
    has_major_event_7d: bool = False
    event_description: Optional[str] = None
    days_to_earnings: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'ticker': self.ticker,
            'next_earnings_date': self.next_earnings_date.isoformat() if self.next_earnings_date else None,
            'earnings_bmo_amc': self.earnings_bmo_amc,
            'headlines': self.headlines,
            'sentiment_score': self.sentiment_score,
            'has_major_event_7d': self.has_major_event_7d,
            'event_description': self.event_description,
            'days_to_earnings': self.days_to_earnings
        }


@dataclass
class SignalBundle:
    """Combined signals for a ticker."""
    ticker: str
    fund_bias: float  # -10 to 10 (negative = bearish, positive = bullish)
    premium_bias: float  # -10 to 10 (negative = low premium, positive = high premium)
    catalyst_score: float  # 0 to 10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'ticker': self.ticker,
            'fund_bias': self.fund_bias,
            'premium_bias': self.premium_bias,
            'catalyst_score': self.catalyst_score
        }


@dataclass
class RankedIdea:
    """Final ranked trading idea with strategy."""
    ticker: str
    score: float  # Overall score 0-10
    signals: SignalBundle
    options: OptionsSnapshot
    fundamentals: Fundamentals
    catalyst: Catalyst
    strategy: str  # e.g., "BULL PUT SPREAD", "LONG CALL"
    notes: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def bias_direction(self) -> str:
        """Get bias direction string."""
        if self.signals.fund_bias > 2:
            return "BULLISH"
        elif self.signals.fund_bias < -2:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'ticker': self.ticker,
            'score': self.score,
            'bias_direction': self.bias_direction,
            'signals': self.signals.to_dict(),
            'options': self.options.to_dict(),
            'fundamentals': self.fundamentals.to_dict(),
            'catalyst': self.catalyst.to_dict(),
            'strategy': self.strategy,
            'notes': self.notes,
            'timestamp': self.timestamp.isoformat()
        }

