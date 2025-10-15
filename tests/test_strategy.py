"""
Tests for strategy picker.
"""
import pytest
from options_bot.models import SignalBundle, OptionsSnapshot
from options_bot.strategy import pick_strategy


class TestStrategyPicker:
    """Tests for pick_strategy function."""
    
    def test_bullish_high_premium(self):
        """Test bullish bias with high premium."""
        signals = SignalBundle(
            ticker="TEST",
            fund_bias=7.0,  # Bullish
            premium_bias=6.0,  # High premium
            catalyst_score=3.0
        )
        
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.20,
            atm_iv_dte35=0.30,
            iv_rank_1y=75.0,
            skew_25d_rr=0.05,
            term_slope_iv=None,
            liq_calls_score=8.0,
            liq_puts_score=8.0
        )
        
        strategy, notes = pick_strategy(signals, opts)
        assert "BULL PUT SPREAD" in strategy or "SPREAD" in strategy
        assert "premium" in notes.lower()
    
    def test_bullish_low_premium(self):
        """Test bullish bias with low premium."""
        signals = SignalBundle(
            ticker="TEST",
            fund_bias=7.0,  # Bullish
            premium_bias=-6.0,  # Low premium
            catalyst_score=3.0
        )
        
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.30,
            atm_iv_dte35=0.18,
            iv_rank_1y=20.0,
            skew_25d_rr=0.02,
            term_slope_iv=None,
            liq_calls_score=8.0,
            liq_puts_score=8.0
        )
        
        strategy, notes = pick_strategy(signals, opts)
        assert "CALL" in strategy
        assert "cheap" in notes.lower() or "buy" in notes.lower()
    
    def test_bearish_high_premium(self):
        """Test bearish bias with high premium."""
        signals = SignalBundle(
            ticker="TEST",
            fund_bias=-7.0,  # Bearish
            premium_bias=6.0,  # High premium
            catalyst_score=2.0
        )
        
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.20,
            atm_iv_dte35=0.32,
            iv_rank_1y=80.0,
            skew_25d_rr=0.06,
            term_slope_iv=None,
            liq_calls_score=7.0,
            liq_puts_score=7.0
        )
        
        strategy, notes = pick_strategy(signals, opts)
        assert "BEAR CALL SPREAD" in strategy or "CALL SPREAD" in strategy
    
    def test_neutral_high_premium(self):
        """Test neutral bias with high premium."""
        signals = SignalBundle(
            ticker="TEST",
            fund_bias=0.5,  # Neutral
            premium_bias=7.0,  # High premium
            catalyst_score=2.0
        )
        
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.18,
            atm_iv_dte35=0.32,
            iv_rank_1y=85.0,
            skew_25d_rr=0.04,
            term_slope_iv=None,
            liq_calls_score=9.0,
            liq_puts_score=9.0
        )
        
        strategy, notes = pick_strategy(signals, opts)
        assert "CONDOR" in strategy or "STRANGLE" in strategy
    
    def test_neutral_low_premium_with_catalyst(self):
        """Test neutral with low premium and catalyst."""
        signals = SignalBundle(
            ticker="TEST",
            fund_bias=1.0,  # Neutral
            premium_bias=-5.0,  # Low premium
            catalyst_score=8.0  # High catalyst
        )
        
        opts = OptionsSnapshot(
            ticker="TEST",
            spot_price=100.0,
            hv30=0.25,
            atm_iv_dte35=0.16,
            iv_rank_1y=15.0,
            skew_25d_rr=0.01,
            term_slope_iv=None,
            liq_calls_score=8.0,
            liq_puts_score=8.0
        )
        
        strategy, notes = pick_strategy(signals, opts)
        assert "STRADDLE" in strategy or "CALENDAR" in strategy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

