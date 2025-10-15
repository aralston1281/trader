## API Keys Setup Guide

This guide will help you obtain free API keys for enhanced data sources. All of these offer free tiers!

## 📊 Priority Order (Start Here)

### 1. **Polygon.io** - Best for Options Data ⭐
**Free Tier**: 5 API calls per minute

1. Go to https://polygon.io/
2. Click "Get Your Free API Key"
3. Sign up with email
4. Verify email
5. Go to Dashboard → API Keys
6. Copy your API key
7. Add to `.env`: `POLYGON_API_KEY=your_key_here`

**What you get**:
- Real-time options data
- Better IV calculations
- Detailed Greeks
- Options flow data
- News feed

---

### 2. **Finnhub** - News & Market Data ⭐
**Free Tier**: 60 calls per minute, real-time data

1. Go to https://finnhub.io/
2. Click "Get free API key"
3. Sign up with email or GitHub
4. Dashboard will show your API key
5. Add to `.env`: `FINNHUB_API_KEY=your_key_here`

**What you get**:
- Company news with sentiment scores
- Earnings calendar
- Market data
- Insider transactions
- Economic calendar

---

### 3. **Alpha Vantage** - Fundamentals & Technicals
**Free Tier**: 5 calls per minute, 500 per day

1. Go to https://www.alphavantage.co/support/#api-key
2. Enter email
3. Click "GET FREE API KEY"
4. Key sent to your email
5. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key_here`

**What you get**:
- Enhanced fundamentals
- Technical indicators
- Forex & crypto data
- Economic indicators

---

### 4. **News API** - Headlines & Articles
**Free Tier**: 100 requests per day

1. Go to https://newsapi.org/register
2. Sign up with email
3. Verify email
4. API key shown on dashboard
5. Add to `.env`: `NEWS_API_KEY=your_key_here`

**What you get**:
- News from 80,000+ sources
- Search by ticker/company
- Historical articles (up to 1 month on free tier)

---

## 🔓 No API Key Needed

### **SEC EDGAR** - Filings
- Completely free, no registration
- Just needs a valid User-Agent header (already configured)
- Rate limited to 10 requests per second

### **FDA API** - Drug Approvals & Trials
- Open FDA API - no key needed
- Track drug approvals, recalls, adverse events
- Perfect for biotech/pharma stocks

---

## 💰 Optional Premium Sources

### **Tradier** - Advanced Options Data
**Free Sandbox**: Full API access with delayed data

1. Go to https://developer.tradier.com/
2. Sign up for developer account
3. Get sandbox API key (free)
4. Add to `.env`: `TRADIER_API_KEY=your_key_here` and `TRADIER_SANDBOX=true`

**What you get**:
- Detailed options chains
- Greeks calculations
- Expirations and strikes
- Paper trading

---

### **Quandl / Nasdaq Data Link** - Alternative Data
**Free Tier**: Limited datasets

1. Go to https://data.nasdaq.com/
2. Sign up
3. Account → API Key
4. Add to `.env`: `QUANDL_API_KEY=your_key_here`

---

### **Benzinga** - Professional News (Premium)
**Paid**: Starts at $25/month

1. Go to https://www.benzinga.com/apis/
2. Choose a plan
3. Get API key
4. Add to `.env`: `BENZINGA_API_KEY=your_key_here`

**What you get**:
- Breaking news
- Analyst ratings
- Squawks and alerts
- FDA calendar

---

## 🎯 Recommended Free Setup

For best results with no cost, get these 4 keys:

1. ✅ **Polygon.io** - Options data
2. ✅ **Finnhub** - News & sentiment
3. ✅ **Alpha Vantage** - Fundamentals
4. ✅ **News API** - Additional news

**Total cost**: $0  
**Setup time**: ~15 minutes  
**Coverage**: ~95% of features

---

## 📝 Adding Keys to .env

Edit your `.env` file:

```bash
# Required for basic functionality
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK

# Free tier API keys (highly recommended)
POLYGON_API_KEY=your_polygon_key_here
FINNHUB_API_KEY=your_finnhub_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_newsapi_key_here

# Optional
TRADIER_API_KEY=your_tradier_key_here
TRADIER_SANDBOX=true
QUANDL_API_KEY=your_quandl_key_here
BENZINGA_API_KEY=your_benzinga_key_here
```

---

## 🔒 Rate Limits & Best Practices

### Free Tier Limits:
- **Polygon**: 5 calls/minute
- **Finnhub**: 60 calls/minute
- **Alpha Vantage**: 5 calls/minute, 500/day
- **News API**: 100 requests/day
- **SEC EDGAR**: 10 requests/second

### Bot's Built-in Rate Limiting:
The bot automatically:
- Spaces out API calls
- Respects rate limits
- Falls back to yfinance if quotas exceeded
- Caches results when possible

### Tips:
1. **Start small**: Test with 5-10 tickers first
2. **Monitor usage**: Check API dashboards
3. **Schedule wisely**: Run scans 2x daily (premarket & mid-morning)
4. **Upgrade if needed**: Most APIs offer paid tiers

---

## 🚀 Testing Your Keys

After adding keys to `.env`, test them:

```bash
# Run a test scan with one ticker
python -m options_bot.runner.scan

# Check logs for API calls
tail -f logs/options_bot.log
```

Look for messages like:
- ✅ "Fetching from Polygon..."
- ✅ "Got news from Finnhub..."
- ✅ "SEC filings retrieved..."

If you see errors:
- Check that keys are correct
- Verify keys are active
- Check rate limits on provider dashboards

---

## 📊 Feature Matrix

| Feature | Free (yfinance only) | With Free APIs | With Premium |
|---------|---------------------|----------------|--------------|
| Basic fundamentals | ✅ | ✅ | ✅ |
| Options data | Limited | ✅ Good | ✅ Excellent |
| IV calculations | Approximate | ✅ Accurate | ✅ Real-time |
| News | Limited | ✅ Comprehensive | ✅ Pro-level |
| SEC filings | ❌ | ✅ | ✅ |
| FDA tracking | ❌ | ✅ | ✅ |
| Sentiment analysis | ❌ | ✅ | ✅ Advanced |
| Technical analysis | ✅ | ✅ | ✅ |
| Real-time data | ❌ | Delayed | ✅ Real-time |

---

## 🆘 Troubleshooting

### "Invalid API key"
- Double-check key in `.env`
- Ensure no extra spaces
- Verify key is activated

### "Rate limit exceeded"
- Reduce number of tickers
- Increase time between scans
- Check provider dashboard for limits

### "No data returned"
- Some tickers may not be available
- Check provider coverage
- Try with major tickers first (SPY, AAPL, MSFT)

### Keys not loading
- Ensure `.env` file exists
- Check file is in project root
- Restart the bot after editing `.env`

---

## 🎓 Next Steps

1. **Get Discord webhook** (required) - see DISCORD_SETUP.md
2. **Get free API keys** (follow this guide)
3. **Test with 5 tickers** - make sure everything works
4. **Expand your universe** - add more tickers gradually
5. **Monitor and optimize** - adjust based on API usage

---

## 💡 Pro Tips

1. **Stagger your requests**: The bot does this automatically
2. **Cache when possible**: Store results in database
3. **Use webhooks**: Some APIs support webhooks for events
4. **Monitor costs**: Even "free" tiers can have overages
5. **Have backups**: If one API is down, bot falls back to others

---

## 📚 API Documentation Links

- **Polygon**: https://polygon.io/docs
- **Finnhub**: https://finnhub.io/docs/api
- **Alpha Vantage**: https://www.alphavantage.co/documentation/
- **News API**: https://newsapi.org/docs
- **SEC EDGAR**: https://www.sec.gov/edgar/sec-api-documentation
- **FDA**: https://open.fda.gov/apis/
- **Tradier**: https://documentation.tradier.com/

---

## ⚠️ Important Notes

1. **Never commit API keys to git** - they're in `.gitignore`
2. **Don't share keys publicly** - they're tied to your account
3. **Rotate keys periodically** - for security
4. **Read ToS carefully** - especially for commercial use
5. **Monitor usage** - avoid surprise charges

---

## 🎉 Ready to Go!

With free API keys, you'll get:
- ✅ Professional-grade options analysis
- ✅ Comprehensive news coverage
- ✅ SEC filing alerts
- ✅ FDA tracking for biotech
- ✅ Enhanced catalyst detection
- ✅ Better IV/Greeks calculations

All for **$0/month**! 🚀

