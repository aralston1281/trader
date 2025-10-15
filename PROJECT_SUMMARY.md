# Options Bot Framework - Project Summary

## Overview

A complete, production-ready options trading ideas generator that automatically analyzes stocks and provides ranked trading opportunities twice daily via Discord notifications.

## What Was Built

### Core Features ✅

1. **Multi-Factor Analysis**
   - Fundamental analysis (P/E, margins, debt, growth)
   - Options structure analysis (IV/HV, IV rank, skew, liquidity)
   - Catalyst detection (earnings, news, sentiment)

2. **Automated Strategy Selection**
   - 10+ options strategies mapped to market conditions
   - Intelligent selection based on bias + premium environment
   - Detailed reasoning for each recommendation

3. **Scheduled Execution**
   - Premarket scan (5:30 AM ET)
   - Mid-morning scan (9:45 AM ET)
   - Monday-Friday only (respects market schedule)

4. **Discord Notifications**
   - Rich formatted messages with embeds
   - Color-coded by bias (green/red/gray)
   - Detailed metrics and strategy notes

5. **Flexible Configuration**
   - Environment-based settings
   - Custom ticker universe
   - Adjustable scoring weights
   - Liquidity and market cap filters

## Project Structure

```
options_bot/
├── options_bot/
│   ├── __init__.py
│   ├── models.py              # Data models
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Configuration management
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── fundamentals.py    # yfinance fundamentals
│   │   ├── options.py         # Options data + IV/HV calculations
│   │   └── catalysts.py       # Earnings + news + sentiment
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── fundamental.py     # Fundamental bias scoring
│   │   ├── premium.py         # Premium structure bias
│   │   └── catalyst.py        # Catalyst scoring
│   ├── ranker/
│   │   ├── __init__.py
│   │   └── ranker.py          # Combine signals + rank
│   ├── strategy/
│   │   ├── __init__.py
│   │   └── picker.py          # Strategy selection logic
│   ├── notify/
│   │   ├── __init__.py
│   │   ├── discord_notifier.py  # Discord webhook
│   │   ├── email_notifier.py    # SMTP email
│   │   └── formatter.py         # Output formatting
│   └── runner/
│       ├── __init__.py
│       ├── __main__.py
│       ├── scan.py            # Main orchestration
│       └── scheduler.py       # APScheduler integration
├── tests/
│   ├── __init__.py
│   ├── test_signals.py        # Signal function tests
│   ├── test_strategy.py       # Strategy picker tests
│   └── test_smoke.py          # Integration tests
├── config/
│   └── universe.csv           # Ticker list
├── scripts/
│   └── init_project.py        # Initialization helper
├── .env.example               # Configuration template
├── .gitignore
├── requirements.txt
├── setup.py
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── options-bot.service        # systemd service
├── LICENSE                    # MIT License
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick start guide
├── DISCORD_SETUP.md          # Discord webhook setup
└── PROJECT_SUMMARY.md        # This file
```

## Technology Stack

### Core Libraries
- **pandas** / **numpy** - Data manipulation
- **yfinance** - Market data (free)
- **APScheduler** - Task scheduling
- **requests** - HTTP/Discord webhooks
- **python-dotenv** - Configuration management

### Optional Enhancements
- **transformers** - FinBERT sentiment analysis
- **sqlalchemy** - Historical data storage
- **feedparser** - RSS news feeds

### Testing
- **pytest** - Unit and integration tests
- **pytest-cov** - Code coverage

## Key Algorithms

### 1. Fundamental Bias (-10 to +10)
- Scores based on valuation (P/E, Forward P/E)
- Profitability (margins, growth)
- Financial health (debt-to-equity)
- Positive = bullish, Negative = bearish

### 2. Premium Bias (-10 to +10)
- IV/HV ratio (primary factor)
- IV rank (percentile over 1 year)
- Put/call skew analysis
- Term structure slope
- Positive = high premium (sell), Negative = low premium (buy)

### 3. Catalyst Score (0 to 10)
- Earnings proximity (±5 days = highest)
- News sentiment (if FinBERT enabled)
- Major event detection
- Higher = more catalysts

### 4. Overall Ranking
- Weighted combination: 60% fundamental, 25% premium, 15% catalyst
- Liquidity penalties for illiquid options
- Market cap filters
- Top N ideas selected (default: 10)

### 5. Strategy Selection
Decision matrix based on:
- Directional bias (bullish/bearish/neutral)
- Premium level (high/low/moderate)
- Catalyst proximity

Examples:
- Bullish + High Premium → Bull Put Spread
- Bearish + Low Premium → Long Put
- Neutral + High Premium → Iron Condor
- Neutral + Low Premium + Catalyst → Long Straddle

## Configuration Options

### Environment Variables (.env)

**Required:**
- `DISCORD_WEBHOOK_URL` - Your Discord webhook URL

**Optional:**
- `UNIVERSE_CSV` - Path to ticker list
- `RUN_PREMARKET` - Premarket scan time (default: 05:30)
- `RUN_MIDMORNING` - Mid-morning scan time (default: 09:45)
- `WEIGHT_FUNDAMENTAL` - Fundamental weight (default: 0.6)
- `WEIGHT_PREMIUM` - Premium weight (default: 0.25)
- `WEIGHT_CATALYST` - Catalyst weight (default: 0.15)
- `MAX_PICKS` - Number of ideas to show (default: 10)
- `MIN_LIQUIDITY_SCORE` - Minimum liquidity (default: 3.0)
- `MIN_MARKET_CAP` - Minimum market cap (default: $1B)

### Universe Configuration

Edit `config/universe.csv` to customize tickers:

```csv
ticker,enabled
AAPL,true
MSFT,true
YOUR_TICKER,true
SKIP_THIS,false
```

## Usage

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize project
python scripts/init_project.py

# 3. Configure Discord webhook in .env

# 4. Run a test scan
python -m options_bot.runner.scan

# 5. Start the scheduler
python -m options_bot.runner.scheduler
```

### Manual Scans

```bash
# Default scan
python -m options_bot.runner.scan

# Custom scan name
python -m options_bot.runner.scan "Evening Scan"
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=options_bot

# Fast tests only (skip slow API calls)
pytest -m "not slow"
```

## Deployment Options

### 1. Local Machine
```bash
python -m options_bot.runner.scheduler
```

### 2. Docker
```bash
docker-compose up -d
```

### 3. Linux Service (systemd)
```bash
sudo cp options-bot.service /etc/systemd/system/
sudo systemctl enable options-bot
sudo systemctl start options-bot
```

### 4. Cloud VM (AWS/DigitalOcean/etc.)
```bash
nohup python -m options_bot.runner.scheduler > output.log 2>&1 &
```

## Extensibility

### Add New Data Sources

Implement new providers in `ingestion/`:
```python
def get_options_snapshot_polygon(ticker: str) -> OptionsSnapshot:
    # Fetch from Polygon.io API
    pass
```

### Add Custom Signals

Create new scoring functions in `signals/`:
```python
def technical_bias(ticker: str, timeframe: str) -> float:
    # Analyze technical indicators
    pass
```

### Customize Strategies

Modify `strategy/picker.py` to add new strategies or adjust selection logic.

### Add New Notification Channels

Create new notifiers in `notify/`:
```python
def send_slack(webhook_url: str, ideas: List[RankedIdea]) -> bool:
    # Send to Slack
    pass
```

## Future Enhancements (Phase 2)

- [ ] Integrate Polygon.io for real-time options Greeks
- [ ] Add Tradier API for detailed options chains
- [ ] Backtesting engine with P&L tracking
- [ ] Position sizing recommendations
- [ ] Web dashboard for monitoring
- [ ] Machine learning signal enhancement
- [ ] Multi-leg strategy Greeks calculations
- [ ] Risk management rules
- [ ] Paper trading integration
- [ ] Performance analytics

## Data Sources

### Current (Free)
- **yfinance** - Stock fundamentals, price history, options chains, earnings dates, news

### Future (Paid/Premium)
- **Polygon.io** - Real-time options data, Greeks, accurate IV
- **Tradier** - Advanced options analytics
- **Alpha Vantage** - Additional fundamentals
- **News APIs** - Better news coverage and sentiment

## Limitations & Disclaimers

### Current Limitations
1. **yfinance data** - Free but may be delayed or incomplete
2. **IV calculations** - Approximations without Greeks
3. **Sentiment analysis** - Requires FinBERT model (optional)
4. **Earnings timing** - BMO/AMC not always available
5. **Backtesting** - Not yet implemented

### Important Disclaimers
⚠️ **This software is for educational and research purposes only.**

- Not financial advice
- Options trading involves substantial risk
- Past performance doesn't guarantee future results
- Always do your own due diligence
- Consider consulting a financial advisor

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Areas of interest:
- Additional data source integrations
- Enhanced signal algorithms
- New strategy templates
- Backtesting framework
- Web interface
- Performance improvements

## Support

- **Documentation**: See README.md and QUICKSTART.md
- **Discord Setup**: See DISCORD_SETUP.md
- **Issues**: Check logs in `logs/options_bot.log`
- **Testing**: Run `pytest -v` to verify installation

## Acknowledgments

Built following the Options Bot Framework specification with:
- Clean, modular architecture
- Production-ready code quality
- Comprehensive documentation
- Extensible design patterns
- Best practices for Python projects

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: October 2025

