# Quick Start Guide

Get the Options Bot running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Discord account (for notifications)
- Internet connection

## Installation

### 1. Clone or Download

```bash
cd options_bot
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set Up Discord Webhook

Follow the instructions in `DISCORD_SETUP.md` to get your webhook URL.

### 2. Create `.env` File

```bash
cp .env.example .env
```

### 3. Edit `.env`

Open `.env` in a text editor and update:

```env
# REQUIRED: Add your Discord webhook URL
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE

# OPTIONAL: Customize these if desired
MAX_PICKS=10
MIN_MARKET_CAP=1000000000
```

### 4. Review Universe

The default ticker list is in `config/universe.csv`. Edit to add/remove tickers:

```csv
ticker,enabled
AAPL,true
MSFT,true
YOUR_TICKER,true
```

## Running the Bot

### Manual Scan (Test It Out)

```bash
python -m options_bot.runner.scan
```

This will:
1. Fetch data for all tickers in your universe
2. Analyze fundamentals, options, and catalysts
3. Rank the best opportunities
4. Send results to Discord

### Start the Scheduler (Automatic Scans)

```bash
python -m options_bot.runner.scheduler
```

This will:
- Run automatically at 5:30 AM ET (premarket)
- Run automatically at 9:45 AM ET (mid-morning)
- Run Monday-Friday only
- Keep running until you stop it (Ctrl+C)

## What to Expect

After running a scan, you'll see a Discord message like:

```
📊 Options Picks - Morning Scan
🕐 2025-10-15 05:30 ET

🟢 1. AAPL - BULLISH (Score: 8.5/10)
   📈 IV/HV: 1.25 (IV Rank: 75%)
   💧 Liquidity: High
   📰 Catalyst: Earnings in 3 days
   🎯 Strategy: BULL PUT SPREAD
   📝 Strong fundamentals, collect premium pre-earnings
```

## Customization

### Change Scan Times

Edit `.env`:
```env
RUN_PREMARKET=05:30
RUN_MIDMORNING=09:45
```

### Adjust Scoring Weights

Edit `.env`:
```env
WEIGHT_FUNDAMENTAL=0.6    # 60% weight
WEIGHT_PREMIUM=0.25       # 25% weight
WEIGHT_CATALYST=0.15      # 15% weight
```

### Filter Settings

Edit `.env`:
```env
MIN_LIQUIDITY_SCORE=3.0   # Skip low liquidity options
MIN_MARKET_CAP=1000000000 # Skip stocks under $1B market cap
MAX_PICKS=10              # Number of ideas to show
```

## Running 24/7

### Option 1: Leave Computer On

Just keep the scheduler running in a terminal window.

### Option 2: Cloud VM

Deploy to a cloud server (AWS EC2, DigitalOcean, etc.):

```bash
# On the server
nohup python -m options_bot.runner.scheduler > output.log 2>&1 &
```

### Option 3: Docker

```bash
docker-compose up -d
```

### Option 4: Linux Service (systemd)

```bash
sudo cp options-bot.service /etc/systemd/system/
sudo systemctl enable options-bot
sudo systemctl start options-bot
```

## Troubleshooting

### "No module named 'options_bot'"

Make sure:
1. Virtual environment is activated
2. You're in the project root directory
3. Dependencies are installed: `pip install -r requirements.txt`

### No Discord messages

1. Check webhook URL is correct in `.env`
2. Verify `USE_DISCORD=true` in `.env`
3. Look at logs: `logs/options_bot.log`

### "No tickers in universe"

Check that `config/universe.csv` exists and has enabled tickers.

### Slow Performance

- Reduce number of tickers in universe
- yfinance can be slow; consider upgrading to paid APIs later

### No data for certain tickers

Some tickers may not have complete data via yfinance. This is normal. The bot will skip them and continue with others.

## Next Steps

- Read the full README.md for more details
- Customize signal weights and strategy rules
- Add more tickers to your universe
- Set up backtesting (coming soon)
- Integrate paid data APIs for better options data

## Getting Help

- Check logs in `logs/options_bot.log`
- Review the full documentation in README.md
- Check Discord webhook setup in DISCORD_SETUP.md

## Disclaimer

This software is for educational purposes only. Always do your own research before trading options. Options trading involves substantial risk.

