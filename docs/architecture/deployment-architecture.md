# 🐳 Deployment Architecture - Rowell Infra

> **Containerized deployment architecture for African fintech infrastructure**

## 📋 Overview

The Rowell Infra deployment architecture is designed for scalability, reliability, and ease of management using Docker containerization and modern DevOps practices.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                    │
├─────────────────────────────────────────────────────────────┤
│  Port 8080 (HTTP)    Port 8443 (HTTPS)                     │
│  SSL Termination     Rate Limiting                         │
│  Request Routing     CORS Handling                         │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Rowell API          Frontend (React)                      │
│  Port 8000           Port 3000                             │
│  FastAPI             Vite Dev Server                       │
│  Async Workers       Hot Reload                            │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  Background Services                        │
├─────────────────────────────────────────────────────────────┤
│  Celery Worker       Celery Beat                           │
│  Async Tasks         Scheduled Tasks                       │
│  Blockchain Sync     Analytics Processing                  │
│  Webhook Delivery    Email Notifications                   │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL          Redis Cache                           │
│  Port 5433           Port 6381                             │
│  Primary Database    Session & Cache                       │
│  Connection Pool     Task Queue                            │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  Monitoring Stack                           │
├─────────────────────────────────────────────────────────────┤
│  Prometheus          Grafana                               │
│  Port 9091           Port 3000                             │
│  Metrics Collection  Dashboards                            │
│  Alerting Rules      Visualization                         │
└─────────────────────────────────────────────────────────────┘
```

## 🐳 Docker Services

### Core Services Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: rowell-postgres
    environment:
      POSTGRES_DB: rowell_infra
      POSTGRES_USER: rowell
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rowell -d rowell_infra"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - rowell-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: rowell-redis
    ports:
      - "6381:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - rowell-network

  # Rowell API
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: rowell-api
    environment:
      - DATABASE_URL=postgresql+asyncpg://rowell:${POSTGRES_PASSWORD}@postgres:5432/rowell_infra
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=${DEBUG:-false}
      - SECRET_KEY=${SECRET_KEY}
    ports:
      - "8000:8000"
    volumes:
      - ./api:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - rowell-network

  # Celery Worker
  celery-worker:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: rowell-celery-worker
    command: celery -A api.core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://rowell:${POSTGRES_PASSWORD}@postgres:5432/rowell_infra
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=${DEBUG:-false}
    volumes:
      - ./api:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - rowell-network

  # Celery Beat
  celery-beat:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: rowell-celery-beat
    command: celery -A api.core.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://rowell:${POSTGRES_PASSWORD}@postgres:5432/rowell_infra
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=${DEBUG:-false}
    volumes:
      - ./api:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - rowell-network

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: rowell-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_API_KEY=${API_KEY}
    depends_on:
      - api
    networks:
      - rowell-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: rowell-nginx
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api
      - frontend
    networks:
      - rowell-network

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: rowell-prometheus
    ports:
      - "9091:9090"
    volumes:
      - ./docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - rowell-network

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: rowell-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./docker/grafana/provisioning:/etc/grafana/provisioning
      - ./docker/grafana/dashboards:/var/lib/grafana/dashboards
    networks:
      - rowell-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  rowell-network:
    driver: bridge
```

## 🔧 Dockerfile Configurations

### API Dockerfile

```dockerfile
# api/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "run", "dev"]
```

## 🌐 Nginx Configuration

### Nginx Reverse Proxy

```nginx
# docker/nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=frontend:10m rate=30r/s;

    server {
        listen 80;
        server_name localhost;

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend routes
        location / {
            limit_req zone=frontend burst=50 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://api/health;
        }
    }

    # HTTPS configuration
    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend routes
        location / {
            limit_req zone=frontend burst=50 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## 📊 Monitoring Configuration

### Prometheus Configuration

```yaml
# docker/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'rowell-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Rowell Infra Dashboard",
    "panels": [
      {
        "title": "API Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(rowell_requests_total[5m])",
            "legendFormat": "{{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(rowell_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Active Accounts",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rowell_active_accounts",
            "legendFormat": "Active Accounts"
          }
        ]
      }
    ]
  }
}
```

## 🔒 Security Configuration

### Environment Variables

```bash
# .env
# Database
POSTGRES_PASSWORD=secure_password_here
DATABASE_URL=postgresql+asyncpg://rowell:secure_password_here@postgres:5432/rowell_infra

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
API_KEY=sk_test_1234567890

# Monitoring
GRAFANA_PASSWORD=secure_grafana_password

# Blockchain
STELLAR_TESTNET_URL=https://horizon-testnet.stellar.org
HEDERA_TESTNET_URL=https://testnet.mirrornode.hedera.com

# Debug
DEBUG=false
```

### SSL/TLS Configuration

```bash
# Generate SSL certificates for development
openssl req -x509 -newkey rsa:4096 -keyout docker/nginx/ssl/key.pem -out docker/nginx/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

## 🚀 Deployment Commands

### Development Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Production Deployment

```bash
# Production environment
docker-compose -f docker-compose.prod.yml up -d

# Health checks
curl http://localhost:8080/health

# Monitor services
docker-compose ps
```

## 📈 Scaling Configuration

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  api:
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=postgresql+asyncpg://rowell:${POSTGRES_PASSWORD}@postgres:5432/rowell_infra
      - REDIS_URL=redis://redis:6379/0

  celery-worker:
    deploy:
      replicas: 5
    environment:
      - DATABASE_URL=postgresql+asyncpg://rowell:${POSTGRES_PASSWORD}@postgres:5432/rowell_infra
      - REDIS_URL=redis://redis:6379/0
```

### Load Balancer Configuration

```yaml
# nginx load balancer
upstream api {
    server api_1:8000;
    server api_2:8000;
    server api_3:8000;
}

upstream frontend {
    server frontend_1:3000;
    server frontend_2:3000;
}
```

## 🔧 Health Checks

### Service Health Checks

```bash
#!/bin/bash
# health-check.sh

# Check API health
curl -f http://localhost:8000/health || exit 1

# Check database connection
docker-compose exec postgres pg_isready -U rowell -d rowell_infra || exit 1

# Check Redis connection
docker-compose exec redis redis-cli ping || exit 1

# Check Celery worker
docker-compose exec celery-worker celery -A api.core.celery inspect ping || exit 1

echo "All services healthy"
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh

while true; do
    echo "=== Rowell Infra Health Check ==="
    echo "Timestamp: $(date)"
    
    # API health
    if curl -s -f http://localhost:8000/health > /dev/null; then
        echo "✅ API: Healthy"
    else
        echo "❌ API: Unhealthy"
    fi
    
    # Database health
    if docker-compose exec -T postgres pg_isready -U rowell -d rowell_infra > /dev/null 2>&1; then
        echo "✅ Database: Healthy"
    else
        echo "❌ Database: Unhealthy"
    fi
    
    # Redis health
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis: Healthy"
    else
        echo "❌ Redis: Unhealthy"
    fi
    
    echo "================================"
    sleep 30
done
```

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Environment variables configured
- [ ] SSL certificates generated
- [ ] Database migrations ready
- [ ] Health checks implemented
- [ ] Monitoring configured

### Deployment

- [ ] Docker images built
- [ ] Services started
- [ ] Health checks passing
- [ ] Load balancer configured
- [ ] SSL/TLS enabled

### Post-Deployment

- [ ] Monitoring dashboards active
- [ ] Logs being collected
- [ ] Backup strategy implemented
- [ ] Alerting configured
- [ ] Performance benchmarks met

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
