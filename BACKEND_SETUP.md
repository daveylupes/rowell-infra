# Backend Setup & Running Instructions

This guide provides step-by-step instructions for setting up and running the Rowell Infra backend API on Ubuntu/Linux and Windows.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Ubuntu/Linux Setup](#ubuntulinux-setup)
- [Windows Setup](#windows-setup)
- [Manual Setup (All Platforms)](#manual-setup-all-platforms)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### All Platforms

- **Python 3.8+** (Python 3.10 or 3.11 recommended)
- **pip** (Python package installer)
- **Git** (optional, for cloning the repository)

### Optional (for Production)

- **PostgreSQL** (for production database)
- **Redis** (for caching and Celery tasks)

---

## Ubuntu/Linux Setup

### Quick Start (Automated Script)

1. **Navigate to the API directory:**
   ```bash
   cd rowell-infra/api
   ```

2. **Make the startup script executable:**
   ```bash
   chmod +x start-backend.sh
   ```

3. **Run the startup script:**
   ```bash
   ./start-backend.sh
   ```

The script will automatically:
- Check for Python installation
- Create a virtual environment
- Install all dependencies
- Initialize the database
- Start the backend server

### Manual Setup (Ubuntu/Linux)

If you prefer to set up manually or the script doesn't work:

1. **Update system packages:**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Install Python and required packages:**
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Navigate to the API directory:**
   ```bash
   cd rowell-infra/api
   ```

4. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

5. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

6. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

7. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

8. **Set up environment variables:**
   ```bash
   # If .env doesn't exist, create it from the example
   cp ../env.example ../.env
   # Edit the .env file with your configuration
   nano ../.env
   ```

9. **Initialize the database (if needed):**
   ```bash
   python manage_db.py init
   ```

10. **Run the backend:**
    ```bash
    python main.py
    ```

---

## Windows Setup

### Option 1: PowerShell Script (Recommended)

1. **Open PowerShell as Administrator**

2. **Enable script execution (first time only):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Navigate to the API directory:**
   ```powershell
   cd rowell-infra\api
   ```

4. **Run the PowerShell startup script:**
   ```powershell
   .\start-backend.ps1
   ```

### Option 2: Batch Script

1. **Open Command Prompt**

2. **Navigate to the API directory:**
   ```cmd
   cd rowell-infra\api
   ```

3. **Run the batch startup script:**
   ```cmd
   start-backend.bat
   ```

### Manual Setup (Windows)

If you prefer manual setup:

1. **Install Python:**
   - Download from [python.org](https://www.python.org/downloads/)
   - **Important:** Check "Add Python to PATH" during installation

2. **Open Command Prompt or PowerShell**

3. **Navigate to the API directory:**
   ```cmd
   cd rowell-infra\api
   ```

4. **Create a virtual environment:**
   ```cmd
   python -m venv venv
   ```

5. **Activate the virtual environment:**
   - **Command Prompt:**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

6. **Upgrade pip:**
   ```cmd
   python -m pip install --upgrade pip
   ```

7. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

8. **Set up environment variables:**
   ```cmd
   # Copy the example file
   copy ..\env.example ..\.env
   # Edit .env with your preferred text editor
   notepad ..\.env
   ```

9. **Initialize the database (if needed):**
   ```cmd
   python manage_db.py init
   ```

10. **Run the backend:**
    ```cmd
    python main.py
    ```

---

## Manual Setup (All Platforms)

### Using uvicorn directly

For more control over the server configuration:

```bash
# Activate virtual environment first (see platform-specific instructions above)

# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables

Key environment variables (edit `.env` file):

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db  # For development
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rowell_infra  # For production

# Security
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true

# CORS (add your frontend URLs)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Network URLs
STELLAR_TESTNET_URL=https://horizon-testnet.stellar.org
HEDERA_TESTNET_URL=https://testnet.mirrornode.hedera.com
```

---

## Verification

After starting the backend, verify it's running:

### 1. Check the Server

Open your browser and navigate to:

- **API Root:** [http://localhost:8000](http://localhost:8000)
- **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

### 2. Test with curl (Ubuntu/Linux/macOS)

```bash
curl http://localhost:8000/health
```

### 3. Test with PowerShell (Windows)

```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## Troubleshooting

### Common Issues

#### 1. "Python not found" or "command not found"

**Ubuntu/Linux:**
```bash
sudo apt install python3 python3-pip
```

**Windows:**
- Reinstall Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

#### 2. "Permission denied" (Ubuntu/Linux)

Make the script executable:
```bash
chmod +x start-backend.sh
```

#### 3. "Execution Policy" error (Windows PowerShell)

Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Port 8000 already in use

Find and kill the process using port 8000:

**Ubuntu/Linux:**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Or change the port in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

#### 5. Database connection errors

**PostgreSQL Connection Refused:**

If you see `ConnectionRefusedError: [Errno 111] Connection refused`, the backend is trying to connect to PostgreSQL but it's not running.

**For Development (SQLite):**
The startup scripts automatically use SQLite (no PostgreSQL needed). If this still happens:

```bash
# Manually set the database URL to SQLite
export DATABASE_URL="sqlite+aiosqlite:///./rowell_infra_dev.db"  # Linux/Mac
set DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db       # Windows CMD
$env:DATABASE_URL="sqlite+aiosqlite:///./rowell_infra_dev.db"    # Windows PowerShell

# Then run
python main.py
```

**For Production (PostgreSQL):**
If you need PostgreSQL:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib  # Ubuntu
# Or download from https://www.postgresql.org/download/ for Windows

# Create database
sudo -u postgres createdb rowell_infra

# Update .env with your PostgreSQL credentials
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/rowell_infra
```

#### 6. Module import errors

Make sure you're in the `api/` directory and the virtual environment is activated:

```bash
# Check current directory
pwd  # Should end with /api

# Check if virtual environment is activated
which python  # Should point to venv/bin/python or venv\Scripts\python
```

#### 7. Dependency installation fails

Try upgrading pip first:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Getting Help

If you continue to experience issues:

1. Check the console output for specific error messages
2. Ensure all prerequisites are installed
3. Verify your Python version: `python --version` (should be 3.8+)
4. Check the logs in the console output
5. Open an issue on the project repository with:
   - Your operating system and version
   - Python version
   - Full error message
   - Steps you've already tried

---

## Next Steps

Once the backend is running:

1. **Explore the API documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Set up the frontend:** See `frontend/README.md`
3. **Run the test suite:** `pytest` (with virtual environment activated)
4. **Configure for production:** See `docs/architecture/deployment-architecture.md`

---

## Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Project README](../README.md)
- [Development Guide](../docs/guides/developer-guide.md)
- [Deployment Guide](../docs/architecture/deployment-architecture.md)

