"""
Tests for signal functions.
"""
import pytest
from options_bot.models import Fundamentals, OptionsSnapshot, Catalyst
from options_bot.signals import fundamental_bias, premium_bias, catalyst_score
from datetime import datetime, timedelta


class TestFundamentalBias:
    """Tests for fundamental_bias function."""
    
    def test_bullish_fundamentals(self):
        """Test bullish fundamental scoring."""
        fund = Fundamentals(
            ticker="TEST",
            market_cap=10e9,
            pe_ratio=12.0,  # Low P/E
            forward_pe=10.0,
            profit_margins=0.25,  # High margins
            debt_to_equity=0.2,  # Low debt
            sector="Technology",
            revenue_growth=0.25,  # Strong growth
            earnings_growth=0.30
        )
        
        score = fundamental_bias(fund)
        assert score > 5, "Should be strongly bullish"
    
    def test_bearish_fundamentals(self):
        """Test bearish fundamental scoring."""
        fund = Fundamentals(
            ticker="TEST",
            market_cap=10e9,
            pe_ratio=70.0,  # High P/E
            forward_pe=65.0,
            profit_margins=-0.05,  # Negative margins
            debt_to_equity=3.5,  # High debt
            sector="Technology",
            revenue_growth=-0.15,  # Declining revenue
            earnings_growth=-0.20
        )
        
        score = fundamental_bias(fund)
        assert score < -5, "Should be strongly bearish"
    
    def test_neutral_fundamentals(self):
        """Test neutral fundamental scoring."""
        fund = Fundamentals(
            ticker="TEST",
            market_cap=10e9,
            pe_ratio=20.0,
            forward_pe=18.0,
            profit_margins=0.10,
            debt_to_equity=0.8,
            sector="Technology"
        )
        
        score = fundamental_bias(fund)
        assert -3 < score < 3, "Should be relatively neutral"


class TestPremiumBias:
    """Tests for premium_bias function."""
    
    def test_high_premium(self):
        """Test high premium scoring."""
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.20,
            atm_iv_dte35=0.35,  # High IV relative to HV
            iv_rank_1y=85.0,  # High IV rank
            skew_25d_rr=0.08,
            term_slope_iv=None,
            liq_calls_score=8.0,
            liq_puts_score=8.0
        )
        
        score = premium_bias(opts)
        assert score > 5, "Should indicate high premium"
    
    def test_low_premium(self):
        """Test low premium scoring."""
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.30,
            atm_iv_dte35=0.18,  # Low IV relative to HV
            iv_rank_1y=15.0,  # Low IV rank
            skew_25d_rr=-0.02,
            term_slope_iv=None,
            liq_calls_score=8.0,
            liq_puts_score=8.0
        )
        
        score = premium_bias(opts)
        assert score < -5, "Should indicate low premium"


class TestCatalystScore:
    """Tests for catalyst_score function."""
    
    def test_near_earnings(self):
        """Test scoring with near-term earnings."""
        cat = Catalyst(
            ticker="TEST",
            next_earnings_date=datetime.now() + timedelta(days=2),
            earnings_bmo_amc="AMC",
            headlines=["Company announces new product", "Strong quarter expected"],
            sentiment_score=0.6,
            has_major_event_7d=True,
            event_description="Earnings in 2 days",
            days_to_earnings=2
        )
        
        score = catalyst_score(cat)
        assert score > 6, "Should have high catalyst score"
    
    def test_no_catalysts(self):
        """Test scoring with no catalysts."""
        cat = Catalyst(
            ticker="TEST",
            next_earnings_date=None,
            earnings_bmo_amc=None,
            headlines=[],
            sentiment_score=None,
            has_major_event_7d=False,
            event_description=None,
            days_to_earnings=None
        )
        
        score = catalyst_score(cat)
        assert score < 2, "Should have low catalyst score"
    
    def test_distant_earnings(self):
        """Test scoring with distant earnings."""
        cat = Catalyst(
            ticker="TEST",
            next_earnings_date=datetime.now() + timedelta(days=45),
            earnings_bmo_amc="BMO",
            headlines=[],
            sentiment_score=None,
            has_major_event_7d=False,
            event_description=None,
            days_to_earnings=45
        )
        
        score = catalyst_score(cat)
        assert score < 3, "Should have modest catalyst score"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

