# Rowell Infra Backend Startup Script for Windows PowerShell
# This script sets up and starts the FastAPI backend server

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Blue
Write-Host "    Rowell Infra Backend Startup Script" -ForegroundColor Blue
Write-Host "=====================================================" -ForegroundColor Blue
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip *>$null
Write-Host "[OK] pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "[OK] Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check if .env file exists
if (-not (Test-Path "../.env")) {
    Write-Host "No .env file found. Creating from env.example..." -ForegroundColor Yellow
    if (Test-Path "../env.example") {
        Copy-Item "../env.example" "../.env"
        Write-Host "[OK] Created .env file from template" -ForegroundColor Green
        Write-Host "[WARNING] Please edit ../.env with your configuration" -ForegroundColor Yellow
    } else {
        Write-Host "[WARNING] No .env file found. Using development defaults." -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] .env file found" -ForegroundColor Green
}
Write-Host ""

# Check if database exists
if (-not (Test-Path "rowell_infra_dev.db")) {
    Write-Host "Initializing development database..." -ForegroundColor Yellow
    try {
        python manage_db.py init 2>$null
    } catch {
        Write-Host "[WARNING] Database init skipped" -ForegroundColor Yellow
    }
    Write-Host "[OK] Database initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Database already exists" -ForegroundColor Green
}
Write-Host ""

# Start the server
Write-Host "=====================================================" -ForegroundColor Blue
Write-Host "Starting Rowell Infra Backend Server..." -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Blue
Write-Host "Server URL: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Blue
Write-Host ""

# Set development environment variables
$env:DATABASE_URL = "sqlite+aiosqlite:///./rowell_infra_dev.db"
$env:DEBUG = "true"
$env:SECRET_KEY = "dev-secret-key-change-in-production"

# Set environment and run server
$env:PYTHONPATH = "."
python main.py

