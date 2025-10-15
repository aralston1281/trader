"""
Smoke tests for basic functionality.
"""
import pytest
from options_bot.ingestion import get_fundamentals, get_options_snapshot, get_catalyst


class TestSmokeTests:
    """Basic smoke tests with real tickers."""
    
    @pytest.mark.slow
    def test_fundamentals_spy(self):
        """Test fetching fundamentals for SPY."""
        fund = get_fundamentals("SPY")
        assert fund is not None
        assert fund.ticker == "SPY"
        assert fund.market_cap > 0
    
    @pytest.mark.slow
    def test_options_spy(self):
        """Test fetching options data for SPY."""
        opts = get_options_snapshot("SPY")
        assert opts is not None
        assert opts.ticker == "SPY"
        assert opts.spot_price > 0
        assert opts.liquidity_score > 0
    
    @pytest.mark.slow
    def test_catalyst_aapl(self):
        """Test fetching catalyst data for AAPL."""
        cat = get_catalyst("AAPL")
        assert cat is not None
        assert cat.ticker == "AAPL"
    
    @pytest.mark.slow
    def test_full_pipeline_amd(self):
        """Test full data pipeline for AMD."""
        fund = get_fundamentals("AMD")
        opts = get_options_snapshot("AMD")
        cat = get_catalyst("AMD")
        
        assert fund is not None
        assert opts is not None
        assert cat is not None
        
        # Verify we can access key metrics
        assert fund.market_cap > 0
        if opts.hv30:
            assert opts.hv30 > 0
        if opts.liquidity_score:
            assert opts.liquidity_score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "slow"])

