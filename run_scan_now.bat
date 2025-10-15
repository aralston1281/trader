@echo off
echo ========================================
echo Installing Required Packages...
echo ========================================
echo.

pip install pandas numpy yfinance APScheduler pytz python-dotenv requests beautifulsoup4 lxml feedparser pydantic --quiet --user

echo.
echo ========================================
echo Running Options Scan for Tomorrow...
echo ========================================
echo.

python -m options_bot.runner.scan "Scan for Tomorrow"

echo.
echo ========================================
echo Scan Complete! Check Discord for results.
echo ========================================
pause

