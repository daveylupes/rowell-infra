#!/bin/bash

# Rowell Infra - Local Development Startup Script
# This script sets up and runs both backend and frontend locally

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Rowell Infra - Local Development${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Step 1: Setup Backend
echo -e "${YELLOW}Setting up backend...${NC}"
cd api

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from env.example...${NC}"
    if [ -f "../env.example" ]; then
        cp ../env.example .env
        echo -e "${GREEN}✓ Created .env file. Please update it with your configuration.${NC}"
    else
        echo -e "${YELLOW}⚠️  No env.example found. Creating basic .env...${NC}"
        cat > .env <<EOF
# Database (using SQLite for local development)
DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db

# Redis (optional for local dev)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# Hedera (optional - leave empty for mock mode)
HEDERA_TESTNET_OPERATOR_ID=
HEDERA_TESTNET_OPERATOR_KEY=

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8080"]

# Development
DEBUG=true
EOF
        echo -e "${GREEN}✓ Created .env file with generated secrets${NC}"
    fi
    echo ""
    echo -e "${YELLOW}⚠️  Edit api/.env to add your Hedera credentials if you want real transactions${NC}"
    echo ""
fi

# Initialize database (if needed)
if [ ! -f "rowell_infra_dev.db" ]; then
    echo "Initializing database..."
    python manage_db.py init || echo "Database initialization skipped (will auto-create on first run)"
fi

cd ..
echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Step 2: Setup Frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies (this may take a minute)..."
    npm install
else
    echo "Node modules already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No frontend .env file found. Creating...${NC}"
    cat > .env <<EOF
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_KEY=
EOF
    echo -e "${GREEN}✓ Created frontend/.env file${NC}"
fi

cd ..
echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Step 3: Start services
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting services...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
echo -e "${GREEN}API Docs:${NC}    http://localhost:8000/docs"
echo -e "${GREEN}Health Check:${NC} http://localhost:8000/health"
echo ""
echo -e "${GREEN}Frontend:${NC}    http://localhost:5173"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both services${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Start backend in background
echo -e "${BLUE}Starting backend...${NC}"
cd api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Backend failed to start${NC}"
    exit 1
fi

# Start frontend in background
echo -e "${BLUE}Starting frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 2

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Services are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${GREEN}✓ Backend running (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}✓ Frontend running (PID: $FRONTEND_PID)${NC}"
echo ""
echo -e "${BLUE}Open in your browser:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:5173${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both services${NC}"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

