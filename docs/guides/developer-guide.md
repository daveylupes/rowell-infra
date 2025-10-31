# Developer Guide

> **Complete Development Guide for Rowell Infra**

This guide covers everything developers need to know to build applications using Rowell Infra, from basic setup to advanced integration patterns.

## 🚀 Getting Started

### **Prerequisites**

- **Node.js** 18+ (for JavaScript/TypeScript)
- **Python** 3.8+ (for Python SDK)
- **Dart** 3.0+ (for Flutter SDK)
- **Docker** & **Docker Compose** (for local development)
- **Git** (for version control)

### **Quick Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/rowell-infra/rowell-infra.git
   cd rowell-infra
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Verify the setup**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Access the API documentation**
   Open [http://localhost:8000/docs](http://localhost:8000/docs)

## 📚 SDKs Overview

### **JavaScript/TypeScript SDK**

The most feature-complete SDK with full TypeScript support.

```bash
npm install @rowell/infra-sdk
```

**Basic Usage:**
```typescript
import { RowellClient } from '@rowell/infra-sdk';

const client = new RowellClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key_here'
});

// Create an account
const account = await client.accounts.create({
  network: 'stellar',
  environment: 'testnet',
  accountType: 'user',
  countryCode: 'NG'
});

// Send a transfer
const transfer = await client.transfers.send({
  fromAccount: account.accountId,
  toAccount: 'GDEF456...UVW012',
  asset: 'USDC',
  amount: '100.00'
});
```

### **Python SDK**

Full-featured Python SDK with async support.

```bash
pip install rowell-infra
```

**Basic Usage:**
```python
from rowell_infra import RowellClient

client = RowellClient('http://localhost:8000', 'your_api_key_here')

# Create an account
account = await client.accounts.create(
    network='stellar',
    environment='testnet',
    account_type='user',
    country_code='NG'
)

# Send a transfer
transfer = await client.transfers.send(
    from_account=account['account_id'],
    to_account='GDEF456...UVW012',
    asset='USDC',
    amount='100.00'
)
```

### **Flutter SDK**

Mobile SDK for cross-platform development.

```yaml
dependencies:
  rowell_infra: ^1.0.0
```

**Basic Usage:**
```dart
import 'package:rowell_infra/rowell_infra.dart';

final client = RowellClient(
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key_here',
);

// Create an account
final account = await client.accounts.create(
  network: 'stellar',
  environment: 'testnet',
  accountType: 'user',
  countryCode: 'NG',
);

// Send a transfer
final transfer = await client.transfers.send(
  fromAccount: account.accountId,
  toAccount: 'GDEF456...UVW012',
  asset: 'USDC',
  amount: '100.00',
);
```

## 🏗️ Architecture Overview

### **System Components**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Rowell API    │    │   Blockchains   │
│   (React/Vue)   │◄──►│   (FastAPI)     │◄──►│   Stellar       │
│                 │    │                 │    │   Hedera        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   + Analytics   │
                       └─────────────────┘
```

### **Key Design Principles**

1. **Unified API**: Single interface for both Stellar and Hedera
2. **African-First**: Built specifically for African markets
3. **Developer Experience**: Easy integration with comprehensive SDKs
4. **Scalability**: Designed to handle high transaction volumes
5. **Compliance**: Built-in KYC/AML for regulatory compliance

## 🔧 Development Workflow

### **1. Local Development**

**Start the development stack:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

**Services available:**
- **API**: http://localhost:8000
- **Frontend**: http://localhost:8080
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9091

### **2. API Development**

**Interactive Documentation:**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Testing Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Create account
curl -X POST http://localhost:8000/api/v1/accounts/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG"
  }'
```

### **3. Frontend Development**

**Start the frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Available at:** http://localhost:8080

### **4. Database Management**

**Access PostgreSQL:**
```bash
# Connect to database
docker exec -it rowell-postgres psql -U rowell -d rowell_infra

# Run migrations
docker exec -it rowell-api alembic upgrade head

# Reset database
docker exec -it rowell-api alembic downgrade base
```

## 📊 Data Models

### **Account Model**

```typescript
interface Account {
  id: string;
  accountId: string;        // Stellar public key or Hedera account ID
  network: 'stellar' | 'hedera';
  environment: 'testnet' | 'mainnet';
  accountType: 'user' | 'merchant' | 'anchor' | 'ngo';
  countryCode?: string;     // ISO 2-letter country code
  region?: string;          // Regional grouping
  isActive: boolean;
  isVerified: boolean;
  isCompliant: boolean;
  kycStatus: 'pending' | 'verified' | 'rejected';
  createdAt: string;
  updatedAt: string;
  lastActivity?: string;
  metadata?: Record<string, any>;
}
```

### **Transfer Model**

```typescript
interface Transfer {
  id: string;
  transferId: string;
  transactionHash: string;
  status: 'pending' | 'success' | 'failed';
  fromAccount: string;
  toAccount: string;
  assetCode: string;
  assetIssuer?: string;
  amount: string;
  network: 'stellar' | 'hedera';
  environment: 'testnet' | 'mainnet';
  fromCountry?: string;
  toCountry?: string;
  memo?: string;
  feeCharged: string;
  createdAt: string;
  completedAt?: string;
}
```

### **Analytics Models**

```typescript
interface RemittanceFlow {
  fromCountry: string;
  toCountry: string;
  period: string;
  totalVolumeUsd: number;
  transactionCount: number;
  averageTransactionSize: number;
  growthRate: number;
}

interface StablecoinAdoption {
  asset: string;
  countryCode: string;
  period: string;
  totalVolumeUsd: number;
  uniqueUsers: number;
  adoptionRate: number;
  growthRate: number;
}
```

## 🔐 Authentication & Security

### **API Key Management**

**Getting API Keys:**
1. **Testnet**: Available immediately after signup
2. **Mainnet**: Requires verification and approval
3. **Enterprise**: Contact support for custom limits

**Using API Keys:**
```typescript
const client = new RowellClient({
  baseUrl: 'http://localhost:8000',
  apiKey: process.env.ROWELL_API_KEY
});
```

**Environment Variables:**
```bash
# .env
ROWELL_API_URL=http://localhost:8000
ROWELL_API_KEY=your_api_key_here
ROWELL_NETWORK=both
ROWELL_ENVIRONMENT=testnet
```

### **Security Best Practices**

1. **Never commit API keys to version control**
2. **Use environment variables for configuration**
3. **Implement proper error handling**
4. **Validate all user inputs**
5. **Use HTTPS in production**

## 🌍 African Market Integration

### **Country Support**

```typescript
const SUPPORTED_COUNTRIES = {
  NG: { name: 'Nigeria', currency: 'NGN', idType: 'BVN' },
  KE: { name: 'Kenya', currency: 'KES', idType: 'National ID' },
  ZA: { name: 'South Africa', currency: 'ZAR', idType: 'SA ID' },
  GH: { name: 'Ghana', currency: 'GHS', idType: 'Ghana Card' },
  UG: { name: 'Uganda', currency: 'UGX', idType: 'National ID' },
  TZ: { name: 'Tanzania', currency: 'TZS', idType: 'National ID' }
};
```

### **Local Compliance**

**KYC Verification:**
```typescript
const verification = await client.compliance.verifyId({
  accountId: 'user_account_id',
  verificationType: 'individual',
  firstName: 'John',
  lastName: 'Doe',
  documentType: 'national_id',
  documentNumber: '1234567890',
  documentCountry: 'NG'
});
```

**Compliance Checking:**
```typescript
const compliance = await client.compliance.checkCompliance({
  accountId: 'user_account_id',
  transactionAmount: '1000.00',
  transactionType: 'transfer'
});
```

## 📈 Analytics Integration

### **Real-time Analytics**

**WebSocket Connection:**
```typescript
const ws = new WebSocket('ws://localhost:8000/ws/analytics');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Analytics update:', data);
};
```

**Remittance Flows:**
```typescript
const flows = await client.analytics.getRemittanceFlows({
  fromCountry: 'NG',
  toCountry: 'KE',
  periodType: 'monthly'
});
```

**Stablecoin Adoption:**
```typescript
const adoption = await client.analytics.getStablecoinAdoption({
  asset: 'USDC',
  countryCode: 'KE',
  periodType: 'monthly'
});
```

## 🧪 Testing

### **Unit Testing**

**JavaScript/TypeScript:**
```typescript
import { RowellClient } from '@rowell/infra-sdk';

describe('RowellClient', () => {
  let client: RowellClient;

  beforeEach(() => {
    client = new RowellClient({
      baseUrl: 'http://localhost:8000',
      apiKey: 'test_api_key'
    });
  });

  it('should create an account', async () => {
    const account = await client.accounts.create({
      network: 'stellar',
      environment: 'testnet',
      accountType: 'user',
      countryCode: 'NG'
    });

    expect(account.accountId).toBeDefined();
    expect(account.network).toBe('stellar');
  });
});
```

**Python:**
```python
import pytest
from rowell_infra import RowellClient

@pytest.fixture
def client():
    return RowellClient('http://localhost:8000', 'test_api_key')

@pytest.mark.asyncio
async def test_create_account(client):
    account = await client.accounts.create(
        network='stellar',
        environment='testnet',
        account_type='user',
        country_code='NG'
    )
    
    assert account['account_id'] is not None
    assert account['network'] == 'stellar'
```

### **Integration Testing**

**Test Environment Setup:**
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
npm run test:integration

# Cleanup
docker-compose -f docker-compose.test.yml down
```

### **Load Testing**

**Using Artillery:**
```yaml
# artillery-config.yml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "Create Account"
    flow:
      - post:
          url: "/api/v1/accounts/create"
          headers:
            Authorization: "Bearer test_api_key"
          json:
            network: "stellar"
            environment: "testnet"
            account_type: "user"
            country_code: "NG"
```

## 🚀 Deployment

### **Production Deployment**

**Environment Configuration:**
```bash
# Production environment variables
export ROWELL_ENVIRONMENT=mainnet
export ROWELL_API_URL=https://api.rowell-infra.com
export ROWELL_API_KEY=your_production_key
export DATABASE_URL=postgresql://user:pass@host:port/db
export REDIS_URL=redis://host:port/0
```

**Docker Deployment:**
```bash
# Build production image
docker build -t rowell-infra:latest .

# Deploy with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

**Cloud Deployment:**
- **AWS**: ECS, EKS, Lambda
- **Azure**: Container Instances, AKS
- **Google Cloud**: Cloud Run, GKE

### **Monitoring & Observability**

**Health Checks:**
```typescript
const health = await client.getHealth();
console.log('API Status:', health.status);
```

**Metrics Collection:**
```typescript
// Custom metrics
const metrics = {
  accountCreations: 0,
  transfersProcessed: 0,
  errorRate: 0
};

// Update metrics
metrics.accountCreations++;
```

## 🔧 Troubleshooting

### **Common Issues**

**1. Connection Refused**
```bash
# Check if services are running
docker-compose ps

# Check logs
docker-compose logs api
```

**2. Authentication Errors**
```typescript
// Verify API key
const health = await client.getHealth();
if (!health) {
  console.error('Invalid API key or network issue');
}
```

**3. Transaction Failures**
```typescript
// Check account balance
const account = await client.accounts.get(accountId);
console.log('Account balance:', account.balances);

// Check network status
const networkInfo = await client.getNetworkInfo();
console.log('Network status:', networkInfo);
```

### **Debug Mode**

**Enable Debug Logging:**
```typescript
const client = new RowellClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key',
  debug: true  // Enable debug logging
});
```

**View API Logs:**
```bash
# Follow API logs
docker-compose logs -f api

# Filter for specific logs
docker-compose logs api | grep "ERROR"
```

## 📚 Additional Resources

### **Documentation**
- [API Reference](api-reference.md)
- [SDK Documentation](sdk-documentation.md)
- [Integration Examples](integration-examples.md)

### **Community**
- [Discord](https://discord.gg/rowell-infra) - Developer community
- [GitHub](https://github.com/rowell-infra/rowell-infra) - Source code and issues
- [Twitter](https://twitter.com/rowell_infra) - Updates and news

### **Support**
- [GitHub Issues](https://github.com/rowell-infra/rowell-infra/issues) - Bug reports
- [Email Support](mailto:support@rowell-infra.com) - Direct support
- [Documentation Issues](https://github.com/rowell-infra/rowell-infra/discussions) - Documentation feedback

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
