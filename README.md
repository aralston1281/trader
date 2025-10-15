# Options Picks Bot Framework

A comprehensive automated options trading ideas generator that analyzes fundamentals, catalysts, and options structure to provide daily ranked trading opportunities.

## Features

- 🎯 **Daily Scans**: Automated runs at 5:30 AM and 9:45 AM ET
- 📊 **Multi-Factor Analysis**: Combines fundamentals, options structure (IV/HV, liquidity, skew), and catalysts
- 🔔 **Smart Notifications**: Discord webhook or Email delivery
- 📈 **Strategy Recommendations**: Automated options strategy selection based on market conditions
- 🧪 **Backtesting**: Save historical snapshots for performance analysis

## Architecture

```
options_bot/
├── ingestion/       # Data fetching (price, fundamentals, options, catalysts)
├── signals/         # Scoring functions (fundamental, premium, catalyst biases)
├── ranker/          # Signal combination and ranking logic
├── strategy/        # Options strategy selection
├── runner/          # Orchestration and scheduling
├── notify/          # Notification formatting and delivery
├── config/          # Configuration and settings management
└── tests/           # Unit and integration tests
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/options_bot.git
cd options_bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required: DISCORD_WEBHOOK_URL
```

### 3. Set Up Discord Webhook

1. Go to your Discord server settings
2. Navigate to Integrations → Webhooks
3. Click "New Webhook"
4. Copy the webhook URL and paste it into your `.env` file

### 4. Configure Your Universe

Edit `config/universe.csv` to add the tickers you want to scan:

```csv
ticker,enabled
AAPL,true
MSFT,true
TSLA,true
AMD,true
```

### 5. Run the Bot

```bash
# Manual scan
python -m options_bot.runner.scan

# Start scheduler (runs at configured times)
python -m options_bot.runner.scheduler
```

## Output Example

**Discord Message:**

```
📊 Options Picks - Morning Scan
🕐 2025-10-15 05:30 ET

🟢 1. AAPL - BULLISH (Score: 8.5/10)
   📈 IV/HV: 1.25 (Elevated premium)
   💧 Liquidity: High
   📰 Catalyst: Earnings in 3 days
   🎯 Strategy: BULL PUT SPREAD
   📝 Strong fundamentals, collect premium pre-earnings

🔴 2. TSLA - BEARISH (Score: 7.8/10)
   📈 IV/HV: 0.85 (Low premium)
   💧 Liquidity: High
   📰 Catalyst: Product launch tomorrow
   🎯 Strategy: LONG PUT
   📝 Overvalued, negative skew, buy puts cheap

⚪ 3. SPY - NEUTRAL (Score: 6.5/10)
   📈 IV/HV: 1.10 (Moderate premium)
   💧 Liquidity: Very High
   📰 Catalyst: None
   🎯 Strategy: IRON CONDOR
   📝 Range-bound, collect theta
```

## Data Models

- **Fundamentals**: Market cap, P/E ratios, margins, debt metrics, sector
- **OptionsSnapshot**: Spot price, HV, IV metrics, IV rank, skew, term structure, liquidity
- **Catalyst**: Earnings dates, major events, news headlines with sentiment
- **SignalBundle**: Combined bias scores from all signals
- **RankedIdea**: Final scored and ranked trading idea with strategy

## Algorithms

### Fundamental Bias
- Lower P/E + high margins → bullish
- High debt-to-equity → bearish
- Sector momentum considered

### Premium Bias
- IV/HV ratio analysis
- IV rank (1-year percentile)
- Put/call skew
- Term structure slope
- Liquidity scoring

### Catalyst Scoring
- Earnings proximity (±5 days)
- News sentiment analysis
- Major event detection

### Ranking
Weighted combination:
- Fundamentals: 60%
- Premium structure: 25%
- Catalysts: 15%
- Liquidity penalties applied

## Strategy Selection

Rule-based mapping of signals to strategies:
- High IV + Bullish → Bull Put Spread, Covered Call
- Low IV + Bullish → Long Call, Call Spread
- High IV + Bearish → Bear Call Spread
- Low IV + Bearish → Long Put, Put Spread
- Neutral + High IV → Iron Condor, Straddle Sell
- Neutral + Low IV → Long Straddle, Calendar Spread

## Configuration

Key environment variables in `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_WEBHOOK_URL` | Discord webhook for notifications | Yes |
| `UNIVERSE_CSV` | Path to ticker list CSV | Yes |
| `TIMEZONE` | Timezone for scheduling (default: America/New_York) | No |
| `RUN_PREMARKET` | Premarket scan time (HH:MM) | No |
| `RUN_MIDMORNING` | Mid-morning scan time (HH:MM) | No |
| `USE_FINBERT` | Enable AI sentiment analysis | No |
| `MIN_MARKET_CAP` | Minimum market cap filter | No |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=options_bot tests/

# Run specific test
pytest tests/test_signals.py
```

## Extending the Framework

### Add Custom Data Sources
Implement providers in `ingestion/` following the base interfaces.

### Add Custom Signals
Create new scoring functions in `signals/` module.

### Customize Strategies
Modify the strategy picker in `strategy/picker.py`.

## Deployment

### Local/VM
```bash
# Run in background with nohup
nohup python -m options_bot.runner.scheduler > output.log 2>&1 &
```

### Docker
```bash
docker build -t options-bot .
docker run -d --env-file .env options-bot
```

### Systemd Service (Linux)
```bash
sudo cp options-bot.service /etc/systemd/system/
sudo systemctl enable options-bot
sudo systemctl start options-bot
```

## Roadmap

- [x] Core framework with yfinance data
- [x] Discord webhook notifications
- [ ] Integrate Polygon.io for real-time options data
- [ ] Add Tradier API for Greeks and complex chains
- [ ] Backtesting engine with P&L tracking
- [ ] Position sizing recommendations
- [ ] Web dashboard for monitoring
- [ ] Machine learning signal enhancement

## Troubleshooting

### "No module named 'options_bot'"
Make sure you're running from the project root and your virtual environment is activated.

### Discord messages not sending
Verify your webhook URL is correct and the webhook is enabled in Discord.

### No data for tickers
Some tickers may not have options data available via yfinance. Consider upgrading to paid APIs.

## Disclaimer

**This software is for educational and research purposes only.** It does not constitute financial advice. Options trading involves substantial risk of loss. Always perform your own due diligence and consult with a financial advisor before making any trading decisions.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

