# Quick Start Guide - Rowell Infra

Get up and running with Rowell Infra in minutes!

## 🚀 Quick Start

### Backend (API Server)

#### Ubuntu/Linux
```bash
cd rowell-infra/api
./start-backend.sh
```

#### Windows (PowerShell)
```powershell
cd rowell-infra\api
.\start-backend.ps1
```

#### Windows (Command Prompt)
```cmd
cd rowell-infra\api
start-backend.bat
```

**Access the API:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

### Frontend (React App)

#### All Platforms
```bash
cd rowell-infra/frontend
npm install          # First time only
npm run dev         # Development server
# or
npm run build       # Production build
```

**Access the Frontend:**
- Development: http://localhost:5173
- After build: Serve files from `frontend/dist/`

---

## 📋 Prerequisites

### All Users Need:
- **Python 3.8+** for backend
- **Node.js 16+** and **npm** for frontend
- **Git** (optional)

### Ubuntu/Linux:
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install Node.js (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Windows:
- Download Python: https://www.python.org/downloads/
  - ✅ Check "Add Python to PATH"
- Download Node.js: https://nodejs.org/

---

## 🔧 First-Time Setup

### 1. Clone the Repository (if not already done)
```bash
git clone <repository-url>
cd rowell-infra
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit with your settings (optional for development)
nano .env  # or use any text editor
```

### 3. Run Backend (see commands above)

### 4. Run Frontend (see commands above)

---

## ✅ Verification

### Backend Running?
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","version":"0.1.0",...}`

### Frontend Running?
Open browser: http://localhost:5173

---

## 📚 Full Documentation

- **Backend Setup Details:** [BACKEND_SETUP.md](./BACKEND_SETUP.md)
- **Frontend Setup:** [frontend/README.md](./frontend/README.md)
- **Project Overview:** [README.md](./README.md)
- **Developer Guide:** [docs/guides/developer-guide.md](./docs/guides/developer-guide.md)

---

## 🆘 Common Issues

### "Python not found"
- **Windows:** Reinstall Python with "Add to PATH" checked
- **Ubuntu:** `sudo apt install python3`

### "Port 8000 already in use"
```bash
# Find and kill the process
sudo lsof -i :8000        # Linux
netstat -ano | findstr :8000  # Windows
```

### "Permission denied" on Linux
```bash
chmod +x api/start-backend.sh
```

### Dependencies won't install
```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm cache clean --force
npm install
```

---

## 🎯 What's Next?

1. ✅ Start backend server
2. ✅ Start frontend development server  
3. 📖 Explore API docs: http://localhost:8000/docs
4. 💻 Review example code in `docs/examples.py`
5. 🧪 Run tests: `pytest` (in api directory)
6. 🚢 Deploy to production (see deployment guides)

---

## 💡 Development Tips

- **Backend auto-reload:** Enabled by default in development
- **Frontend hot-reload:** Built into Vite (npm run dev)
- **API Testing:** Use the interactive docs at http://localhost:8000/docs
- **Database:** SQLite used by default for development (no setup needed)

---

**Happy Coding! 🎉**

For detailed instructions, troubleshooting, and production deployment, see [BACKEND_SETUP.md](./BACKEND_SETUP.md).

