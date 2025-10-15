# Installing TA-Lib (Technical Analysis Library)

TA-Lib can be tricky to install. Here's how to do it on different platforms.

## Windows

### Option 1: Pre-built Wheel (Easiest)

1. Download the wheel for your Python version from:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

2. Choose the right file:
   - Python 3.11, 64-bit: `TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl`
   - Python 3.10, 64-bit: `TA_Lib‑0.4.28‑cp310‑cp310‑win_amd64.whl`
   - Python 3.9, 64-bit: `TA_Lib‑0.4.28‑cp39‑cp39‑win_amd64.whl`

3. Install the wheel:
   ```bash
   cd Downloads
   pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl
   ```

4. Verify installation:
   ```python
   python -c "import talib; print('TA-Lib installed successfully!')"
   ```

### Option 2: Using Anaconda

```bash
conda install -c conda-forge ta-lib
```

## macOS

### Using Homebrew:

```bash
# Install TA-Lib C library
brew install ta-lib

# Install Python wrapper
pip install TA-Lib
```

## Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install build-essential wget

# Download and install TA-Lib C library
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
sudo ldconfig

# Install Python wrapper
pip install TA-Lib
```

## Alternative: Use pandas-ta (No compilation needed)

If TA-Lib installation fails, the bot will automatically fall back to `pandas-ta`, which is pure Python and works everywhere:

```bash
pip install pandas-ta
```

**Note**: pandas-ta is already in requirements.txt, so you're covered either way!

## Testing Your Installation

Run this test script:

```python
python -c "
try:
    import talib
    print('✅ TA-Lib installed and working!')
except ImportError:
    print('❌ TA-Lib not installed')
    import pandas_ta as pta
    print('✅ pandas-ta is available as fallback')
"
```

## Troubleshooting

### "No module named 'talib'"
- TA-Lib not installed correctly
- Try pandas-ta instead: `pip install pandas-ta`
- Bot will work fine with pandas-ta

### "Cannot find function 'RSI'"
- TA-Lib C library not installed
- Follow platform-specific instructions above
- Or use pandas-ta fallback

### "Wheel file not found" (Windows)
- Download the correct wheel for your Python version
- Check Python version: `python --version`
- Make sure it's 64-bit: `python -c "import struct; print(struct.calcsize('P') * 8)"`

### Still having issues?
Just use pandas-ta:
```bash
pip install pandas-ta
```

The bot will work perfectly without TA-Lib (it will use pandas-ta automatically).

## Performance Comparison

| Library | Speed | Installation | Features |
|---------|-------|--------------|----------|
| TA-Lib | ⚡ Very Fast | 😫 Hard | 150+ indicators |
| pandas-ta | ⚡ Fast | 😊 Easy | 130+ indicators |

**Recommendation**: Try TA-Lib, but pandas-ta is perfectly fine for this bot!

## What If Neither Works?

The bot will still function! Technical analysis will be disabled, but all other features work:
- Fundamental analysis
- Options structure
- News aggregation
- SEC filings
- FDA tracking
- Catalyst detection

You can disable technical analysis in `.env`:
```bash
USE_TECHNICAL_ANALYSIS=false
```

## Success!

Once installed, you'll have access to professional technical indicators:
- RSI, MACD, Bollinger Bands
- Moving Averages (SMA, EMA)
- ADX, Support/Resistance
- Volume indicators
- And many more!

Happy analyzing! 📈

