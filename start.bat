@echo off
REM Quick start script for Windows

echo ========================================
echo Options Bot Framework
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
) else (
    echo Dependencies already installed.
    echo.
)

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Copying from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and add your DISCORD_WEBHOOK_URL
    echo Press any key to open .env in notepad...
    pause
    notepad .env
    echo.
)

REM Menu
:menu
echo ========================================
echo What would you like to do?
echo ========================================
echo 1. Run a manual scan (test)
echo 2. Start the scheduler (automated scans)
echo 3. Run tests
echo 4. Initialize project
echo 5. Open Discord setup guide
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto scan
if "%choice%"=="2" goto scheduler
if "%choice%"=="3" goto tests
if "%choice%"=="4" goto init
if "%choice%"=="5" goto discord
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:scan
echo.
echo Running manual scan...
echo.
python -m options_bot.runner.scan
echo.
echo Scan complete!
echo.
pause
goto menu

:scheduler
echo.
echo Starting scheduler...
echo This will run automatically at configured times.
echo Press Ctrl+C to stop.
echo.
python -m options_bot.runner.scheduler
goto menu

:tests
echo.
echo Running tests...
echo.
pytest -v
echo.
pause
goto menu

:init
echo.
echo Initializing project...
echo.
python scripts\init_project.py
echo.
pause
goto menu

:discord
echo.
echo Opening Discord setup guide...
start DISCORD_SETUP.md
echo.
pause
goto menu

:end
echo.
echo Goodbye!
deactivate

