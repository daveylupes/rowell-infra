@echo off
REM Rowell Infra Backend Startup Script for Windows
REM This script sets up and starts the FastAPI backend server

setlocal enabledelayedexpansion

echo ====================================================
echo     Rowell Infra Backend Startup Script
echo ====================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found !PYTHON_VERSION!
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Check if .env file exists
if not exist "..\\.env" (
    echo No .env file found. Creating from env.example...
    if exist "..\\env.example" (
        copy "..\\env.example" "..\\.env" >nul
        echo [OK] Created .env file from template
        echo [WARNING] Please edit .env with your configuration
    ) else (
        echo [WARNING] No .env file found. Using development defaults.
    )
) else (
    echo [OK] .env file found
)
echo.

REM Check if database exists
if not exist "rowell_infra_dev.db" (
    echo Initializing development database...
    python manage_db.py init 2>nul || echo [WARNING] Database init skipped
    echo [OK] Database initialized
) else (
    echo [OK] Database already exists
)
echo.

REM Start the server
echo ====================================================
echo Starting Rowell Infra Backend Server...
echo ====================================================
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo ====================================================
echo.

REM Set development environment variables
set DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db
set DEBUG=true
set SECRET_KEY=dev-secret-key-change-in-production

REM Set PYTHONPATH and run server
set PYTHONPATH=.
python main.py

pause

