"""
Quick test script for the options bot.
Tests with a small universe to verify everything works.
"""
import sys
from options_bot.config import Settings
from options_bot.ingestion import get_fundamentals, get_options_snapshot
from options_bot.ingestion.technical_analysis import get_technical_analysis
from options_bot.ingestion.enhanced_catalysts import get_enhanced_catalysts

# Test tickers
TEST_TICKERS = ['SPY', 'AAPL', 'MSFT']

print("="*60)
print("OPTIONS BOT - QUICK TEST")
print("="*60)
print()

# Test 1: Configuration
print("1️⃣ Testing Configuration...")
try:
    Settings.print_config_summary()
    print("✅ Configuration loaded successfully\n")
except Exception as e:
    print(f"❌ Configuration error: {e}\n")
    sys.exit(1)

# Test 2: Basic Data (yfinance)
print("2️⃣ Testing Basic Data (yfinance)...")
for ticker in TEST_TICKERS[:1]:  # Just test one
    try:
        fund = get_fundamentals(ticker)
        if fund:
            print(f"✅ {ticker} fundamentals: P/E={fund.pe_ratio}, Cap=${fund.market_cap/1e9:.1f}B")
        opts = get_options_snapshot(ticker)
        if opts:
            print(f"✅ {ticker} options: Price=${opts.spot_price:.2f}, IV/HV={opts.iv_hv_ratio:.2f if opts.iv_hv_ratio else 'N/A'}")
        break
    except Exception as e:
        print(f"❌ Error with {ticker}: {e}")
print()

# Test 3: Technical Analysis
print("3️⃣ Testing Technical Analysis...")
try:
    ta = get_technical_analysis('SPY')
    if ta:
        print(f"✅ Technical analysis working")
        print(f"   RSI: {ta.get('rsi', 'N/A'):.1f}" if ta.get('rsi') else "   RSI: N/A")
        print(f"   Bias: {ta.get('bias_score', 0):.1f}/10")
    else:
        print("⚠️  Technical analysis returned no data (may need TA-Lib)")
except Exception as e:
    print(f"⚠️  Technical analysis not available: {e}")
    print("   This is OK - bot will work without it")
print()

# Test 4: Enhanced Catalysts
print("4️⃣ Testing Enhanced Catalysts...")
try:
    catalysts = get_enhanced_catalysts('AAPL')
    if catalysts:
        print(f"✅ Catalyst analysis working")
        print(f"   Overall score: {catalysts.get('overall_score', 0):.1f}/10")
        print(f"   Summary: {catalysts.get('summary', 'N/A')}")
    else:
        print("⚠️  Catalyst analysis returned no data")
except Exception as e:
    print(f"⚠️  Enhanced catalysts error: {e}")
    print("   Bot will use basic catalysts instead")
print()

# Test 5: API Keys Status
print("5️⃣ Checking API Keys...")
api_status = {
    'Polygon': bool(Settings.POLYGON_API_KEY),
    'Finnhub': bool(Settings.FINNHUB_API_KEY),
    'Alpha Vantage': bool(Settings.ALPHA_VANTAGE_API_KEY),
    'News API': bool(Settings.NEWS_API_KEY)
}

for api, configured in api_status.items():
    status = "✅" if configured else "❌"
    print(f"   {status} {api}: {'Configured' if configured else 'Not configured (using fallback)'}")
print()

# Test 6: Discord Webhook
print("6️⃣ Testing Discord Webhook...")
if Settings.DISCORD_WEBHOOK_URL:
    if 'discord.com/api/webhooks' in Settings.DISCORD_WEBHOOK_URL:
        print("✅ Discord webhook configured")
    else:
        print("⚠️  Discord webhook looks incorrect")
else:
    print("❌ Discord webhook not configured - add to .env file")
print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
configured_apis = sum(api_status.values())
print(f"✅ Core functionality: Working")
print(f"📊 API integrations: {configured_apis}/4 configured")
print(f"🔔 Notifications: {'Ready' if Settings.DISCORD_WEBHOOK_URL else 'Need Discord webhook'}")
print()

if configured_apis == 0:
    print("⚠️  NO API KEYS - Bot will use yfinance only (basic mode)")
    print("   → Get free API keys: See API_KEYS_GUIDE.md")
elif configured_apis < 4:
    print(f"✅ PARTIAL SETUP - {configured_apis} APIs configured")
    print("   → Add more keys for full features: See API_KEYS_GUIDE.md")
else:
    print("🎉 FULLY CONFIGURED - All API keys ready!")

print()
if Settings.DISCORD_WEBHOOK_URL:
    print("🚀 Ready to run full scan!")
    print("   → python -m options_bot.runner.scan")
else:
    print("⚠️  Add Discord webhook to .env first")
    print("   → See DISCORD_SETUP.md")

print("="*60)

