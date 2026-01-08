@echo off
echo ====================================
echo PDF Toolkit SaaS - Starting Server
echo ====================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found
    echo Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your Stripe API keys
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo Starting PDF Toolkit SaaS...
echo.
echo ====================================
echo Access the application at:
echo http://localhost:5000
echo ====================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the Flask application
python app.py
