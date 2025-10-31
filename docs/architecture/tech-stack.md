# 🛠️ Technology Stack - Rowell Infra

> **Comprehensive technology stack for African fintech infrastructure**

## 📋 Overview

Rowell Infra uses a modern, scalable technology stack designed for high performance, reliability, and developer experience. The stack is optimized for fintech applications with a focus on African markets.

## 🏗️ Architecture Layers

### Frontend Layer
- **React 18** - Modern UI framework with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Accessible UI primitives

### Backend Layer
- **FastAPI** - High-performance async web framework
- **Python 3.12+** - Latest Python features
- **SQLAlchemy 2.0** - Modern async ORM
- **Pydantic** - Data validation and serialization
- **Celery** - Distributed task queue

### Data Layer
- **PostgreSQL** - Primary relational database
- **Redis** - Caching and session storage
- **Alembic** - Database migration management

### Blockchain Layer
- **Stellar SDK** - Stellar network integration
- **Hedera SDK** - Hedera network integration
- **Web3.py** - Ethereum compatibility (future)

### Infrastructure Layer
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancer
- **Prometheus** - Metrics collection
- **Grafana** - Metrics visualization

## 🔧 Backend Technologies

### Core Framework

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **FastAPI** | Latest | Web framework | Async performance, automatic docs, type safety |
| **Python** | 3.12+ | Programming language | Rich ecosystem, async support, blockchain libraries |
| **Uvicorn** | Latest | ASGI server | High performance, async support |

### Database & Storage

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **PostgreSQL** | 15+ | Primary database | ACID compliance, JSON support, performance |
| **SQLAlchemy** | 2.0+ | ORM | Async support, type safety, migration support |
| **Redis** | 7+ | Cache/Sessions | High performance, data structures, pub/sub |
| **Alembic** | Latest | Migrations | Version control for database schema |

### Task Processing

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **Celery** | 5+ | Task queue | Python integration, scheduling, monitoring |
| **Redis** | 7+ | Message broker | Fast, reliable, persistent |

### Validation & Serialization

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **Pydantic** | 2.0+ | Validation | Type safety, performance, JSON schema |
| **Zod** | 3+ | Schema validation | TypeScript integration, runtime validation |

### Blockchain Integration

| Network | Technology | Purpose | Integration Method |
|---------|------------|---------|-------------------|
| **Stellar** | Stellar SDK | Account creation, transfers | Horizon API |
| **Hedera** | Hedera SDK | Account creation, transfers | Mirror Node API |
| **USDC** | Token Standard | Stablecoin transfers | Multi-network support |

### Monitoring & Observability

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **structlog** | Latest | Structured logging | JSON logging, context, performance |
| **Prometheus** | Latest | Metrics collection | Industry standard, powerful querying |
| **Grafana** | Latest | Visualization | Rich dashboards, alerting |

## 🎨 Frontend Technologies

### Core Framework

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **React** | 18+ | UI framework | Ecosystem, concurrent features, TypeScript |
| **TypeScript** | 5+ | Type system | Type safety, developer experience |
| **Vite** | Latest | Build tool | Fast builds, HMR, modern tooling |

### UI & Styling

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **Radix UI** | Latest | UI primitives | Accessibility, unstyled, composable |
| **Tailwind CSS** | 3+ | CSS framework | Utility-first, performance, customization |
| **Lucide React** | Latest | Icons | Consistent, lightweight, customizable |

### State Management

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **TanStack Query** | 5+ | Server state | Caching, synchronization, background updates |
| **React Hook Form** | 7+ | Form management | Performance, validation, minimal re-renders |
| **Zustand** | Latest | Client state | Simple, TypeScript-friendly |

### Data Visualization

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **Recharts** | 2+ | Charts | React integration, responsive, customizable |
| **D3.js** | Latest | Data manipulation | Powerful, flexible, industry standard |

### Development Tools

| Technology | Version | Purpose | Why Chosen |
|------------|---------|---------|------------|
| **ESLint** | Latest | Linting | Code quality, consistency |
| **Prettier** | Latest | Formatting | Code style, automation |
| **Husky** | Latest | Git hooks | Pre-commit checks, quality gates |

## 🗄️ Database Technologies

### Primary Database

```sql
-- PostgreSQL Configuration
-- Performance optimizations for African fintech queries

-- Indexes for common queries
CREATE INDEX idx_accounts_network_country ON accounts(network, country_code);
CREATE INDEX idx_transactions_from_to ON transactions(from_account_id, to_account_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at DESC);

-- Partitioning for large tables
CREATE TABLE transactions_2024 PARTITION OF transactions
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- JSON support for metadata
CREATE INDEX idx_accounts_metadata_gin ON accounts USING GIN (metadata);
```

### Caching Strategy

```python
# Redis caching patterns
CACHE_PATTERNS = {
    "account": "account:{account_id}",
    "transactions": "transactions:{account_id}:{page}",
    "analytics": "analytics:{type}:{date}",
    "rate_limits": "rate_limit:{api_key}",
}

# Cache TTL configurations
CACHE_TTL = {
    "account": 3600,      # 1 hour
    "transactions": 300,   # 5 minutes
    "analytics": 1800,     # 30 minutes
    "rate_limits": 60,     # 1 minute
}
```

## ⛓️ Blockchain Technologies

### Stellar Integration

```python
# Stellar SDK configuration
from stellar_sdk import Server, Keypair, Network

class StellarService:
    def __init__(self, environment: str):
        if environment == "testnet":
            self.server = Server("https://horizon-testnet.stellar.org")
            self.network = Network.TESTNET_NETWORK_PASSPHRASE
        else:
            self.server = Server("https://horizon.stellar.org")
            self.network = Network.PUBLIC_NETWORK_PASSPHRASE
    
    async def create_account(self) -> StellarAccount:
        # Create keypair
        keypair = Keypair.random()
        
        # Fund account (testnet only)
        if self.network == Network.TESTNET_NETWORK_PASSPHRASE:
            await self._fund_test_account(keypair.public_key)
        
        return StellarAccount(
            account_id=keypair.public_key,
            secret_key=keypair.secret
        )
```

### Hedera Integration

```python
# Hedera SDK configuration
from hedera import Client, PrivateKey, AccountCreateTransaction

class HederaService:
    def __init__(self, environment: str):
        if environment == "testnet":
            self.client = Client.forTestnet()
        else:
            self.client = Client.forMainnet()
    
    async def create_account(self) -> HederaAccount:
        # Generate keypair
        private_key = PrivateKey.generate()
        public_key = private_key.getPublicKey()
        
        # Create account
        response = await AccountCreateTransaction().setKey(public_key).execute(self.client)
        account_id = response.getReceipt(self.client).accountId
        
        return HederaAccount(
            account_id=str(account_id),
            private_key=private_key.toString()
        )
```

## 🐳 Infrastructure Technologies

### Containerization

```dockerfile
# Multi-stage Docker build for production
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim as runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Security: non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Orchestration

```yaml
# Docker Compose for development
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=rowell_infra
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Load Balancing

```nginx
# Nginx load balancer configuration
upstream api_backend {
    least_conn;
    server api1:8000 weight=3;
    server api2:8000 weight=3;
    server api3:8000 weight=2;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring Technologies

### Metrics Collection

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'rowell_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'rowell_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

ACTIVE_ACCOUNTS = Gauge(
    'rowell_active_accounts',
    'Number of active accounts'
)
```

### Logging

```python
# Structured logging with context
import structlog

logger = structlog.get_logger()

async def create_account(self, account_data: AccountCreate):
    logger.info(
        "Creating account",
        network=account_data.network,
        country_code=account_data.country_code,
        request_id=request_id
    )
    
    try:
        account = await self._create_account_logic(account_data)
        logger.info(
            "Account created successfully",
            account_id=account.id,
            duration=time.time() - start_time
        )
        return account
    except Exception as e:
        logger.error(
            "Account creation failed",
            error=str(e),
            network=account_data.network
        )
        raise
```

## 🔒 Security Technologies

### Authentication

```python
# JWT token authentication
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Encryption

```python
# Data encryption for sensitive information
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

## 🧪 Testing Technologies

### Backend Testing

```python
# pytest configuration
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=api
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
```

### Frontend Testing

```typescript
// Jest configuration
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

## 📈 Performance Technologies

### Caching

```python
# Redis caching with TTL
import redis.asyncio as redis

class CacheService:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL)
    
    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, ttl: int = 3600):
        await self.redis.set(key, value, ex=ttl)
    
    async def delete(self, key: str):
        await self.redis.delete(key)
```

### Database Optimization

```python
# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

## 🌍 African Market Technologies

### Localization

```python
# Multi-language support
from babel import Locale, format_currency

AFRICAN_LOCALES = {
    'NG': 'en_NG',  # Nigeria
    'KE': 'en_KE',  # Kenya
    'ZA': 'en_ZA',  # South Africa
    'GH': 'en_GH',  # Ghana
}

def format_local_currency(amount: Decimal, country_code: str):
    locale = Locale.parse(AFRICAN_LOCALES[country_code])
    currency_code = COUNTRY_CURRENCIES[country_code]
    return format_currency(amount, currency_code, locale=locale)
```

### Compliance

```python
# African compliance requirements
AFRICAN_COMPLIANCE = {
    'NG': {
        'kyc_required': True,
        'id_types': ['BVN', 'NIN', 'Passport'],
        'limits': {
            'daily': 500000,  # NGN
            'monthly': 10000000,  # NGN
        }
    },
    'KE': {
        'kyc_required': True,
        'id_types': ['National ID', 'Passport'],
        'limits': {
            'daily': 150000,  # KES
            'monthly': 3000000,  # KES
        }
    }
}
```

## 🔄 CI/CD Technologies

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=api --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📚 Technology Decision Records

### Why FastAPI?

- **Async Performance**: Built-in async/await support for high concurrency
- **Type Safety**: Full type hints with automatic validation
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Standards**: Based on OpenAPI and JSON Schema standards

### Why React?

- **Ecosystem**: Mature ecosystem with extensive tooling
- **Performance**: Concurrent features and optimized rendering
- **TypeScript**: Excellent TypeScript integration
- **Community**: Large community and job market

### Why PostgreSQL?

- **ACID Compliance**: Full ACID compliance for financial data
- **JSON Support**: Native JSON support for flexible schemas
- **Performance**: Excellent performance with proper indexing
- **Reliability**: Battle-tested in production environments

### Why Redis?

- **Performance**: In-memory storage for ultra-fast access
- **Data Structures**: Rich data types for complex use cases
- **Persistence**: Optional persistence for data durability
- **Scalability**: Horizontal scaling with clustering

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Stellar Documentation](https://developers.stellar.org/)
- [Hedera Documentation](https://docs.hedera.com/)

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
