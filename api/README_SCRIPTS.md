# Backend Startup Scripts - README

This directory contains automated startup scripts for running the Rowell Infra backend API server on different operating systems.

## 📁 Available Scripts

### 🐧 Ubuntu/Linux
**File:** `start-backend.sh`

**Usage:**
```bash
chmod +x start-backend.sh  # Make executable (first time only)
./start-backend.sh         # Run the script
```

**Features:**
- ✅ Checks Python installation
- ✅ Creates virtual environment automatically
- ✅ Installs all dependencies
- ✅ Sets up database (SQLite for development)
- ✅ Colored terminal output
- ✅ Auto-activates virtual environment
- ✅ Starts server with auto-reload

---

### 🪟 Windows (Batch Script)
**File:** `start-backend.bat`

**Usage:**
```cmd
start-backend.bat
```

**Best For:** Traditional Windows Command Prompt users

**Features:**
- ✅ Python version check
- ✅ Virtual environment management
- ✅ Dependency installation
- ✅ Database initialization
- ✅ Error handling with pause on completion

---

### 💻 Windows (PowerShell)
**File:** `start-backend.ps1`

**Usage:**
```powershell
# First time: Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the script
.\start-backend.ps1
```

**Best For:** Modern Windows users (Windows 10/11)

**Features:**
- ✅ Advanced error handling
- ✅ Colored console output
- ✅ PowerShell-native commands
- ✅ Better performance than batch
- ✅ All the features of the batch script

---

## 🎯 What These Scripts Do

1. **Environment Check**
   - Verifies Python 3 is installed
   - Shows current Python version

2. **Virtual Environment Setup**
   - Creates `venv/` directory if it doesn't exist
   - Activates the virtual environment
   - Upgrades pip to latest version

3. **Dependency Installation**
   - Installs all packages from `requirements.txt`
   - Includes FastAPI, Uvicorn, database drivers, etc.

4. **Configuration**
   - Checks for `.env` file
   - Creates from `env.example` if missing
   - Warns if configuration needed

5. **Database Setup**
   - Initializes SQLite database for development
   - Creates all necessary tables
   - Skips if database already exists

6. **Server Launch**
   - Starts FastAPI server on port 8000
   - Enables auto-reload in development mode
   - Displays access URLs

---

## 🌐 Access Points After Starting

Once the server is running, you can access:

| Endpoint | URL | Description |
|----------|-----|-------------|
| **API Root** | http://localhost:8000 | API information |
| **Interactive Docs** | http://localhost:8000/docs | Swagger UI |
| **Alternative Docs** | http://localhost:8000/redoc | ReDoc UI |
| **Health Check** | http://localhost:8000/health | Server status |
| **OpenAPI Schema** | http://localhost:8000/api/v1/openapi.json | API schema |

---

## 🛠️ Manual Commands (Alternative)

If you prefer to run commands manually or need more control:

### Activate Virtual Environment

**Ubuntu/Linux:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

### Run Server Manually

```bash
# After activating virtual environment

# Option 1: Using main.py
python main.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Production mode (no reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🔧 Configuration

### Environment Variables

Edit `../.env` to configure:

```bash
# Database (SQLite for dev, PostgreSQL for prod)
DATABASE_URL=sqlite+aiosqlite:///./rowell_infra_dev.db

# Security
SECRET_KEY=your-secret-key-here
DEBUG=true

# CORS (add your frontend URLs)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Blockchain Networks
STELLAR_TESTNET_URL=https://horizon-testnet.stellar.org
HEDERA_TESTNET_URL=https://testnet.mirrornode.hedera.com
```

### Development vs Production

**Development (Default):**
- Uses SQLite database
- Auto-reload enabled
- Debug mode ON
- Single worker process

**Production:**
- PostgreSQL recommended
- Auto-reload disabled
- Debug mode OFF
- Multiple worker processes
- Environment-specific secrets

---

## 📊 Database Management

Use `manage_db.py` for database operations:

```bash
# Initialize database
python manage_db.py init

# Check connection
python manage_db.py check

# Run migrations
python manage_db.py migrate

# Create new migration
python manage_db.py create-migration "Add new feature"

# Show current version
python manage_db.py current

# Show migration history
python manage_db.py history

# Rollback last migration
python manage_db.py rollback
```

---

## 🐛 Troubleshooting

### Script won't run (Ubuntu/Linux)

```bash
# Make it executable
chmod +x start-backend.sh

# Check permissions
ls -la start-backend.sh
```

### PowerShell Execution Policy Error

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8000 Already in Use

**Find the process:**

Ubuntu/Linux:
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

Windows:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Or change the port in main.py:**
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

### Dependencies Won't Install

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Then install dependencies
pip install -r requirements.txt
```

### Import Errors

Make sure you're in the correct directory:
```bash
cd /path/to/rowell-infra/api
pwd  # Should end with /api
```

---

## 📚 Additional Resources

- **Full Setup Guide:** [../BACKEND_SETUP.md](../BACKEND_SETUP.md)
- **Quick Start:** [../QUICK_START.md](../QUICK_START.md)
- **Project README:** [../README.md](../README.md)
- **API Documentation:** http://localhost:8000/docs (when server is running)

---

## 🎓 Script Details

### What's Inside Each Script?

All scripts perform these steps in order:

1. **Pre-flight Checks**
   - Python installation verification
   - Version compatibility check

2. **Environment Setup**
   - Virtual environment creation/activation
   - Pip upgrade

3. **Dependency Management**
   - Read requirements.txt
   - Install all Python packages

4. **Configuration**
   - Environment variable setup
   - .env file creation if needed

5. **Database Initialization**
   - SQLite database creation
   - Table schema creation

6. **Server Launch**
   - Import development config
   - Start Uvicorn with FastAPI app
   - Enable hot-reload for development

---

## 🚀 Next Steps

After the server is running:

1. ✅ Visit http://localhost:8000/docs to explore the API
2. ✅ Test the health endpoint: `curl http://localhost:8000/health`
3. ✅ Set up the frontend (see `../frontend/README.md`)
4. ✅ Read the API documentation
5. ✅ Start building your application!

---

**Questions or Issues?**

Check the full documentation in [BACKEND_SETUP.md](../BACKEND_SETUP.md) or open an issue on the project repository.

