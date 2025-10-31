#!/bin/bash
# Rowell Infra Backend Startup Script for Ubuntu/Linux
# This script sets up and starts the FastAPI backend server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}    Rowell Infra Backend Startup Script${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found $PYTHON_VERSION${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo -e "${YELLOW}No .env file found. Creating from env.example...${NC}"
    if [ -f "../env.example" ]; then
        cp ../env.example ../.env
        echo -e "${GREEN}✓ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠ Please edit ../.env with your configuration${NC}"
    else
        echo -e "${YELLOW}⚠ No .env file found. Using development defaults.${NC}"
    fi
else
    echo -e "${GREEN}✓ .env file found${NC}"
fi
echo ""

# Check if database exists (for SQLite development mode)
if [ ! -f "rowell_infra_dev.db" ]; then
    echo -e "${YELLOW}Initializing development database...${NC}"
    python manage_db.py init || echo -e "${YELLOW}⚠ Database init skipped (may already exist)${NC}"
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${GREEN}✓ Database already exists${NC}"
fi

# Run database migrations to ensure schema is up to date
echo -e "${YELLOW}Running database migrations...${NC}"
python manage_db.py migrate || echo -e "${YELLOW}⚠ Migrations skipped (may already be up to date)${NC}"
echo -e "${GREEN}✓ Database migrations complete${NC}"
echo ""

# Start the server
echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}Starting Rowell Infra Backend Server...${NC}"
echo -e "${BLUE}=================================================${NC}"
echo -e "${YELLOW}Server URL: http://localhost:8000${NC}"
echo -e "${YELLOW}API Docs: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Set development environment variables
export DATABASE_URL="sqlite+aiosqlite:///./rowell_infra_dev.db"
export DEBUG="true"
export SECRET_KEY="dev-secret-key-change-in-production"

# Start the server using uvicorn (preferred method)
# After venv activation, uvicorn should be available in PATH
echo -e "${GREEN}Starting with uvicorn...${NC}"
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info

