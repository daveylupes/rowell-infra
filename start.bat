@echo off
REM Rowell Infra - Local Development Startup Script (Windows)
REM This script sets up and runs both backend and frontend locally

echo ========================================
echo Rowell Infra - Local Development
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    exit /b 1
)

echo Prerequisites check passed
echo.

REM Step 1: Setup Backend
echo Setting up backend...
cd api

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt --quiet

REM Check if .env exists
if not exist .env (
    echo No .env file found. Creating from env.example...
    if exist ..\env.example (
        copy ..\env.example .env >nul
        echo Created .env file. Please update it with your configuration.
    ) else (
        echo Creating basic .env...
        (
            echo # Database ^(using SQLite for local development^)
            echo DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db
            echo.
            echo # Redis ^(optional for local dev^)
            echo REDIS_URL=redis://localhost:6379/0
            echo.
            echo # Security
            echo SECRET_KEY=change-this-in-production
            echo JWT_SECRET_KEY=change-this-in-production
            echo.
            echo # Hedera ^(optional - leave empty for mock mode^)
            echo HEDERA_TESTNET_OPERATOR_ID=
            echo HEDERA_TESTNET_OPERATOR_KEY=
            echo.
            echo # CORS
            echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8080"]
            echo.
            echo # Development
            echo DEBUG=true
        ) > .env
        echo Created .env file with default values
    )
    echo.
    echo Edit api\.env to add your Hedera credentials if you want real transactions
    echo.
)

REM Initialize database (if needed)
if not exist rowell_infra_dev.db (
    echo Initializing database...
    python manage_db.py init || echo Database initialization skipped
)

cd ..
echo Backend setup complete
echo.

REM Step 2: Setup Frontend
echo Setting up frontend...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing Node.js dependencies ^(this may take a minute^)...
    call npm install
) else (
    echo Node modules already installed
)

REM Check if .env exists
if not exist .env (
    echo No frontend .env file found. Creating...
    (
        echo # API Configuration
        echo VITE_API_URL=http://localhost:8000/api/v1
        echo VITE_API_KEY=
    ) > .env
    echo Created frontend\.env file
)

cd ..
echo Frontend setup complete
echo.

REM Step 3: Start services
echo ========================================
echo Starting services...
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Frontend:    http://localhost:5173
echo.
echo Press Ctrl+C to stop both services
echo.

REM Start backend
echo Starting backend...
cd api
start "Rowell Infra Backend" cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend...
cd frontend
start "Rowell Infra Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo Services are running!
echo ========================================
echo.
echo Backend and Frontend started in separate windows
echo Close those windows to stop the services
echo.
echo Open in your browser:
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo.
pause

