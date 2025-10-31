# 🔧 Rowell Infra Installation Guide

This guide provides detailed installation instructions for Rowell Infra in various environments.

## 📋 **System Requirements**

### **Minimum Requirements**
- **OS**: Linux, macOS, or Windows
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+

### **Recommended Requirements**
- **OS**: Ubuntu 20.04+ or macOS 12+
- **RAM**: 16GB
- **Storage**: 10GB free space
- **CPU**: 4+ cores
- **Network**: Stable internet connection

---

## 🐳 **Docker Installation (Recommended)**

### **Step 1: Install Docker**

#### **Ubuntu/Debian**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

#### **macOS**
```bash
brew install docker docker-compose
```

#### **Windows**
Download Docker Desktop from [docker.com](https://docker.com)

### **Step 2: Clone and Start**
```bash
git clone https://github.com/rowell-infra/rowell-infra.git
cd rowell-infra
docker-compose up -d
```

### **Step 3: Verify Installation**
```bash
# Check all services are running
docker-compose ps

# Test the API
curl http://localhost:8000/health
```

---

## 🛠️ **Manual Installation**

### **Step 1: Install Dependencies**

#### **Python 3.11+**
```bash
sudo apt install python3.11 python3.11-venv python3-pip
```

#### **Node.js 18+**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs
```

#### **PostgreSQL 15+**
```bash
sudo apt install postgresql postgresql-contrib
```

#### **Redis**
```bash
sudo apt install redis-server
```

### **Step 2: Set Up Python Environment**
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 3: Set Up Database**
```bash
# Create database
sudo -u postgres createdb rowell_infra

# Run migrations
cd api
alembic upgrade head
```

### **Step 4: Start Services**
```bash
# Start Redis
redis-server

# Start API
cd api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## ⚙️ **Configuration**

### **Environment Variables**

Create a `.env` file in the root directory:

```bash
# API Configuration
ROWELL_API_URL=http://localhost:8000
ROWELL_API_KEY=sk_test_1234567890
ROWELL_NETWORK=both
ROWELL_ENVIRONMENT=testnet

# Database Configuration
DATABASE_URL=postgresql+asyncpg://rowell:rowell@localhost:5432/rowell_infra
REDIS_URL=redis://localhost:6379/0

# Stellar Configuration
STELLAR_TESTNET_URL=https://horizon-testnet.stellar.org
STELLAR_MAINNET_URL=https://horizon.stellar.org
STELLAR_TESTNET_PASSPHRASE=Test SDF Network ; September 2015
STELLAR_MAINNET_PASSPHRASE=Public Global Stellar Network ; September 2015

# Hedera Configuration
HEDERA_TESTNET_URL=https://testnet.mirrornode.hedera.com
HEDERA_MAINNET_URL=https://mainnet-public.mirrornode.hedera.com
HEDERA_TESTNET_NETWORK=testnet
HEDERA_MAINNET_NETWORK=mainnet

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","https://rowell-infra.com"]

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=200

# Compliance
KYC_PROVIDER=mock
COMPLIANCE_WEBHOOK_URL=

# Development
DEBUG=true
```

### **API Keys**

#### **Test API Key (Development)**
```
sk_test_1234567890
```

#### **Production API Key (Get from dashboard)**
```
sk_live_your_production_key_here
```

---

## 🔌 **Service Ports**

| Service | Port | Description |
|---------|------|-------------|
| **API** | 8000 | Main API server |
| **PostgreSQL** | 5433 | Database |
| **Redis** | 6381 | Cache and queues |
| **Grafana** | 3000 | Monitoring dashboard |
| **Prometheus** | 9091 | Metrics collection |
| **Nginx** | 8080 | Load balancer (production) |

---

## ✅ **Verification Steps**

### **1. Health Check**
```bash
curl http://localhost:8000/health
```

### **2. API Documentation**
Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

### **3. Create Test Account**
```bash
curl -X POST "http://localhost:8000/api/v1/accounts/create" \
  -H "Authorization: Bearer sk_test_1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG"
  }'
```

### **4. List Transfers**
```bash
curl -X GET "http://localhost:8000/api/v1/transfers/" \
  -H "Authorization: Bearer sk_test_1234567890"
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Port already in use**
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or change the port in docker-compose.yml
```

#### **Docker permission denied**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### **Database connection failed**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -c "\l"
```

#### **API not responding**
```bash
# Check API logs
docker-compose logs api

# Restart API service
docker-compose restart api
```

### **Logs and Debugging**

#### **View All Logs**
```bash
docker-compose logs
```

#### **View Specific Service Logs**
```bash
docker-compose logs api
docker-compose logs postgres
docker-compose logs redis
```

#### **Follow Logs in Real-time**
```bash
docker-compose logs -f api
```

#### **Debug Mode**
```bash
# Set debug mode
export DEBUG=true

# Restart with debug
docker-compose restart api
```

---

## 🏗️ **Development Setup**

### **For Frontend Developers**

#### **1. Install Node.js Dependencies**
```bash
cd sdk/js
npm install

cd ../../cli
npm install
```

#### **2. Build SDKs**
```bash
# JavaScript SDK
cd sdk/js
npm run build

# CLI Tool
cd cli
npm run build
```

#### **3. Test SDK**
```bash
# Test JavaScript SDK
cd sdk/js
npm test

# Test CLI
cd cli
npm test
```

### **For Backend Developers**

#### **1. Set Up Python Environment**
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **2. Run Tests**
```bash
cd api
pytest
```

#### **3. Run Linting**
```bash
cd api
black .
isort .
mypy .
```

#### **4. Run Database Migrations**
```bash
cd api
alembic upgrade head
```

---

## 🚀 **Production Deployment**

### **Docker Compose Production**

#### **1. Create Production Config**
```bash
cp docker-compose.yml docker-compose.prod.yml
```

#### **2. Update Environment Variables**
```bash
# Set production values
export DATABASE_URL=postgresql://user:pass@prod-db:5432/rowell_infra
export REDIS_URL=redis://prod-redis:6379/0
export SECRET_KEY=your-production-secret-key
export DEBUG=false
```

#### **3. Deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **Cloud Deployment**

#### **AWS ECS**
```bash
# Build and push image
docker build -t rowell-infra .
docker tag rowell-infra:latest your-account.dkr.ecr.region.amazonaws.com/rowell-infra:latest
docker push your-account.dkr.ecr.region.amazonaws.com/rowell-infra:latest

# Deploy to ECS
aws ecs update-service --cluster rowell-cluster --service rowell-api --force-new-deployment
```

#### **Google Cloud Run**
```bash
# Build and push
gcloud builds submit --tag gcr.io/your-project/rowell-infra

# Deploy
gcloud run deploy --image gcr.io/your-project/rowell-infra --platform managed
```

---

## 📊 **Monitoring and Maintenance**

### **Health Checks**

#### **API Health**
```bash
curl http://localhost:8000/health
```

#### **Database Health**
```bash
docker-compose exec postgres pg_isready -U rowell
```

#### **Redis Health**
```bash
docker-compose exec redis redis-cli ping
```

### **Backup and Recovery**

#### **Database Backup**
```bash
docker-compose exec postgres pg_dump -U rowell rowell_infra > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### **Database Restore**
```bash
docker-compose exec -T postgres psql -U rowell -d rowell_infra < backup_file.sql
```

### **Updates and Upgrades**

#### **Update Dependencies**
```bash
# Update Python packages
cd api
pip install --upgrade -r requirements.txt

# Update Node.js packages
cd sdk/js
npm update

# Update Docker images
docker-compose pull
docker-compose up -d
```

---

## 🔒 **Security Considerations**

### **API Keys**
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Use different keys for different environments

### **Database Security**
- Use strong passwords
- Enable SSL connections
- Restrict network access
- Regular security updates

### **Network Security**
- Use HTTPS in production
- Configure proper CORS settings
- Implement rate limiting
- Monitor for suspicious activity

---

## ⚡ **Performance Optimization**

### **Database Optimization**
```sql
-- Create indexes for better performance
CREATE INDEX idx_accounts_country ON accounts(country_code);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_from_account ON transactions(from_account);
```

### **Caching**
```bash
# Redis is already configured for caching
# Check Redis memory usage
docker-compose exec redis redis-cli info memory
```

### **API Optimization**
- Enable gzip compression
- Use connection pooling
- Implement proper pagination
- Cache frequently accessed data

---

## 🎉 **You're All Set!**

Your Rowell Infra development environment is now ready. Here's what you can do next:

1. **Explore the API**: Visit [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Read the Documentation**: Check out our [quickstart guide](quickstart.md)
3. **Join the Community**: [Discord](https://discord.gg/rowell-infra)
4. **Start Building**: Create your first African fintech app!

**Need Help?**
- 📖 [Documentation](../README.md)
- 💬 [Discord Community](https://discord.gg/rowell-infra)
- 🐛 [GitHub Issues](https://github.com/rowell-infra/rowell-infra/issues)
- 📧 [Email Support](mailto:support@rowell-infra.com)

**Happy Building!** 🚀🌍
