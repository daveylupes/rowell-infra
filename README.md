# 🌍 Rowell Infra - Alchemy for Africa

> **Project Track**: Hedera Hackathon - Infrastructure & Developer Tools  
> **Unified Stellar + Hedera APIs & Analytics for African Fintech**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)

## 📋 Project Overview

**Rowell Infra** is an infrastructure platform that simplifies cross-border payments for African fintech applications. We provide unified APIs for both Stellar and Hedera networks, enabling developers to build payment solutions without managing complex blockchain integrations.

### Problem Statement

African cross-border payments face critical challenges:
- **High Fees**: 8-12% transaction costs with traditional methods
- **Slow Settlements**: 3-5 days for completion
- **Complex Integration**: Different APIs for different blockchain networks
- **Compliance Complexity**: Varying KYC/AML requirements across 54 African countries

### Our Solution

- **Unified API**: Single integration supporting Stellar and Hedera networks
- **Low Fees**: 1% transaction fee (90% cheaper than traditional)
- **Fast Settlements**: 3-second transaction completion via Hedera
- **Built-in Compliance**: African-specific KYC/AML tools
- **Developer-First**: Comprehensive SDKs, documentation, and tools

---

## 🔗 Hedera Integration Summary

### Why Hedera for African Fintech?

We chose Hedera Hashgraph as a core blockchain infrastructure for Rowell Infra because its unique features directly address the critical needs of African financial markets:

#### 1. **Hedera Consensus Service (HCS) - Account & Transaction Logging**

**Why**: We use Hedera Mirror Node API for immutable, real-time account and transaction tracking. The predictable $0.0001 fee structure ensures operational cost stability, which is essential for low-margin remittance operations across Africa where every cent saved matters.

**Economic Justification**: 
- Traditional payment providers charge 8-12% fees, making small remittances ($50-200) economically unviable
- Hedera's fixed fees (independent of transaction size) enable us to offer competitive 1% fees
- High throughput (10,000+ TPS) ensures remittance transactions never face network congestion
- ABFT (Asynchronous Byzantine Fault Tolerance) finality provides instant transaction confirmation, critical for real-time remittance tracking that African users expect

**Use Case**: Every account creation and transfer is recorded and queryable via Mirror Node API, providing transparent audit trails required by African financial regulators (CBN, CBK, SARB, etc.).

#### 2. **Hedera Token Service (HTS) - Native HBAR Transfers**

**Why**: While our MVP focuses on HBAR transfers, the architecture supports HTS tokens for stablecoin implementations. Hedera's low transaction fees ($0.0001) enable micro-transactions essential for African markets where users send small amounts frequently.

**Economic Justification**:
- Traditional banks charge minimum fees of $5-10 per international transfer
- Hedera transfers cost $0.0001 regardless of amount, enabling $1-5 remittances economically viable
- Near-zero fees allow us to pass 99% cost savings to end users
- Instant finality (ABFT) means recipients receive funds in seconds, not days

#### 3. **Hedera Smart Contract Service - Future Compliance Automation**

**Why**: Hedera's smart contracts (via EVM compatibility) will enable automated compliance checks and regulatory reporting without the high gas fees of Ethereum. This is critical for operating across multiple African jurisdictions with varying regulations.

**Economic Justification**:
- Ethereum smart contracts cost $5-50+ per execution (unviable for frequent compliance checks)
- Hedera smart contracts cost $0.05-0.50 per execution, making automated compliance economically feasible
- Predictable pricing enables cost-effective multi-jurisdiction operations

---

## 📊 Transaction Types Executed

Our platform executes the following Hedera transactions:

### 1. **AccountCreateTransaction**
- **Purpose**: Create new Hedera accounts for users, merchants, and organizations
- **Execution**: When a developer calls `POST /api/v1/accounts/create` with `network: "hedera"`
- **Fee**: ~$0.05 (one-time account creation fee)
- **Key Properties**:
  - Initial balance: 1 HBAR (minimum required)
  - Public key generated cryptographically
  - Account ID format: `0.0.xxxxxxx`
- **Code Location**: `api/api/services/hedera_service.py:110-131`

### 2. **TransferTransaction**
- **Purpose**: Execute cross-border payments and remittances in HBAR
- **Execution**: When a developer calls `POST /api/v1/transfers/create` for Hedera network
- **Fee**: $0.0001 per transaction (regardless of amount)
- **Key Properties**:
  - From/to account IDs
  - Amount in HBAR (tinybars internally)
  - Transaction memo for compliance tracking
  - Instant finality via ABFT consensus
- **Code Location**: `api/api/services/hedera_service.py:322-360`

### 3. **AccountBalanceQuery**
- **Purpose**: Real-time balance queries for user accounts
- **Execution**: When developers call `GET /api/v1/accounts/{id}/balances`
- **Fee**: Free (query operations have no cost)
- **Key Properties**:
  - Returns balance in HBAR and tinybars
  - Real-time data from Hedera network
  - No query limits (unlike Ethereum's rate-limited RPCs)
- **Code Location**: `api/api/services/hedera_service.py:199-202`

### Additional Hedera Services Used (via Mirror Node API):

4. **Mirror Node Account Info API**: Real-time account information retrieval
   - Endpoint: `GET /api/v1/accounts/{account_id}`
   - Provides: Account creation timestamp, key information, balance history
   - Fee: Free (read-only mirror node queries)

5. **Mirror Node Transaction History**: Transaction history and status tracking
   - Endpoint: `GET /api/v1/transactions`
   - Provides: Complete transaction history for compliance and analytics
   - Fee: Free

---

## 💰 Economic Justification

### Cost Comparison: Traditional vs Hedera

| Feature | Traditional (Western Union) | Hedera via Rowell Infra | Savings |
|---------|---------------------------|-------------------------|---------|
| **Transfer Fee** | 8-12% of amount | 1% flat rate | **92% reduction** |
| **Network Fee** | $5-10 per transaction | $0.0001 (Hedera) | **99.998% reduction** |
| **Settlement Time** | 3-5 days | 3 seconds | **99.99% faster** |
| **Minimum Amount** | $10-50 | No minimum | **Inclusive** |
| **Transaction Finality** | Reversible (up to 180 days) | Instant, irreversible | **Secure** |

### Why This Matters for Africa

1. **Financial Inclusion**: Low fees enable $1-5 remittances economically viable (impossible with traditional methods)
2. **Speed Critical**: Remittances often pay urgent expenses (medical, school fees). 3-second settlement vs 3-5 days is transformative.
3. **Predictable Costs**: Hedera's fixed fees allow us to offer transparent pricing, unlike traditional providers with hidden fees
4. **Scale**: Hedera's 10,000+ TPS handles Africa's growing payment volumes without congestion

---

## 🚀 Deployment & Setup Instructions

### Prerequisites

- **Node.js** 20+ (for frontend)
- **Python** 3.12+ (for backend)
- **PostgreSQL** 14+ (or use Docker)
- **Docker & Docker Compose** (recommended for local development)
- **Git**
- **Hedera Testnet Account** (optional, for real transactions)

### Step-by-Step Setup (Under 10 Minutes)

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rowell-infra.git
cd rowell-infra
```

#### 2. Configure Environment Variables

```bash
# Copy example environment file
cp env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

**Required Environment Variables:**

```bash
# Database (use SQLite for quick testing, PostgreSQL for production)
DATABASE_URL=sqlite+aiosqlite:///./rowell_infra.db

# Hedera Testnet (optional - for real transactions)
HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx  # Get from portal.hedera.com
HEDERA_TESTNET_OPERATOR_KEY=302e...     # Your private key

# Security
SECRET_KEY=generate-strong-secret-key-here
JWT_SECRET_KEY=generate-jwt-secret-key-here

# CORS (add your frontend URL)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

#### 3. Install Dependencies

**Backend:**
```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

#### 4. Initialize Database

```bash
cd api
# Using SQLite (default for development)
python manage_db.py init

# Or using PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/rowell_infra python manage_db.py init
```

#### 5. Run the Backend

```bash
cd api
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Database initialized successfully
INFO:     Application startup complete.
```

#### 6. Run the Frontend

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

#### 7. Verify Installation

```bash
# Test API health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0","timestamp":"..."}

# Open frontend in browser
open http://localhost:5173

# Open API documentation
open http://localhost:8000/docs
```

### Running Environment

**Local Development State:**
- **Frontend**: React app running on `http://localhost:5173` (Vite dev server)
- **Backend API**: FastAPI running on `http://localhost:8000`
- **API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Database**: SQLite (development) or PostgreSQL (production)

### Quick Test

```bash
# Create a Hedera testnet account
curl -X POST "http://localhost:8000/api/v1/accounts/create" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "hedera",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG"
  }'

# Check account balance
curl "http://localhost:8000/api/v1/accounts/{account_id}/balances"
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER / DEVELOPER                        │
│                    (Browser / Mobile App / CLI)                 │
└────────────────────────┬──────────────────────────────────────┘
                          │
                          │ HTTPS / REST API
                          │
         ┌────────────────▼────────────────┐
         │      FRONTEND (React + Vite)    │
         │  - Account Management UI        │
         │  - Transfer Interface           │
         │  - Analytics Dashboard          │
         │  - Developer Portal             │
         │  URL: http://localhost:5173     │
         └────────────────┬────────────────┘
                          │
                          │ REST API Calls
                          │ Authorization: Bearer Token / API Key
                          │
         ┌────────────────▼────────────────┐
         │    ROWELL INFRA API (FastAPI)   │
         │  - Account Service               │
         │  - Transfer Service              │
         │  - Analytics Service             │
         │  - Compliance Service            │
         │  URL: http://localhost:8000      │
         └────────┬───────────────┬─────────┘
                  │               │
        ┌─────────▼────┐  ┌───────▼────────┐
        │  PostgreSQL  │  │     Redis      │
        │  Database    │  │  (Cache/Queue) │
        │              │  │                │
        │ - Accounts   │  │ - Rate Limiting│
        │ - Transfers  │  │ - Sessions     │
        │ - Analytics  │  │ - Job Queue    │
        └──────────────┘  └────────────────┘
                  │
         ┌────────▼──────────────────────────┐
         │    HEDERA NETWORK INTEGRATION      │
         │                                    │
         │  ┌─────────────────────────────┐  │
         │  │  Hedera SDK (Java Bridge)   │  │
         │  │  - AccountCreateTransaction  │  │
         │  │  - TransferTransaction       │  │
         │  │  - AccountBalanceQuery       │  │
         │  └────────────┬────────────────┘  │
         │               │                    │
         │  ┌────────────▼────────────────┐  │
         │  │  Hedera Mirror Node API     │  │
         │  │  - Account Info Queries      │  │
         │  │  - Transaction History       │  │
         │  │  - Balance Queries           │  │
         │  │  URL: testnet.mirrornode.    │  │
         │  │        hedera.com           │  │
         │  └────────────┬────────────────┘  │
         └───────────────┼────────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │   HEDERA TESTNET / MAINNET       │
         │   - Consensus Nodes              │
         │   - Account Storage              │
         │   - Transaction Processing       │
         │   - ABFT Consensus               │
         └──────────────────────────────────┘

Data Flow:
1. User → Frontend: User interacts with React UI
2. Frontend → API: Makes authenticated API calls
3. API → Hedera SDK: Creates/executes transactions
4. Hedera SDK → Hedera Network: Submits transactions
5. Hedera Network: Processes via ABFT consensus (3 seconds)
6. Hedera Mirror Node: Indexes transaction data
7. API ← Mirror Node: Queries account/transaction data
8. API → Database: Stores metadata and analytics
9. API → Frontend: Returns transaction results
10. Frontend → User: Updates UI with results
```

### Key Components

- **Frontend**: React SPA with Vite, communicates with API via REST
- **Backend API**: FastAPI service handling business logic and blockchain integration
- **Hedera SDK**: Python SDK (via Java bridge) for transaction execution
- **Hedera Mirror Node**: Public API for reading account/transaction data
- **Hedera Network**: Consensus nodes processing transactions via ABFT
- **Database**: PostgreSQL for metadata, Redis for caching/queuing

---

## 🔑 Deployed Hedera IDs (Testnet)

**⚠️ Important**: These are testnet IDs for demonstration. Replace with your own testnet credentials for production use.

### Testnet Operator Account
- **Account ID**: `0.0.xxxxxxx` (Configure in `.env` as `HEDERA_TESTNET_OPERATOR_ID`)
- **Network**: Hedera Testnet
- **Purpose**: Operator account for creating new accounts and executing transfers

### Example Test Accounts (Created via API)
When you create accounts through the API, you'll receive Hedera account IDs in format `0.0.xxxxxxx`. Example responses:

```json
{
  "account_id": "0.0.1234567",
  "public_key": "302a300506032b6570032100...",
  "network": "hedera",
  "environment": "testnet",
  "balance": "1.0"
}
```

### Smart Contracts
- Currently not deployed (MVP focuses on account creation and transfers)
- Future: HTS token contracts for stablecoin implementations

### HCS Topics
- Currently not used (MVP uses Mirror Node for transaction tracking)
- Future: Immutable transaction logging for compliance

### HTS Tokens
- Currently using native HBAR for transfers
- Future: USDC/HBAR token transfers via HTS

---

## 🔒 Security & Secrets

### Critical: DO NOT Commit Sensitive Data

**Never commit to git:**
- ❌ `.env` files
- ❌ Private keys (`.pem`, `.key` files)
- ❌ Database passwords
- ❌ API keys with real credentials
- ❌ Hedera operator private keys

**Git-ignored files** (already configured):
- `.env`
- `*.db` (database files)
- `*.key`, `*.pem`
- `venv/`, `node_modules/`
- `.env.*` (all environment files)

### Example Configuration

See `env.example` for the structure of required environment variables:

```bash
# Copy and configure
cp env.example .env

# Required variables:
HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx
HEDERA_TESTNET_OPERATOR_KEY=302e020100300506032b6570...
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=generate-strong-secret-key
```

### Judge Credentials

For hackathon judges to access the deployed application:

1. **API Access**: Test API key provided in DoraHacks submission notes
2. **Frontend**: Deployed at `https://your-domain.com` (no login required for demo)
3. **API Documentation**: Available at `https://api.your-domain.com/docs`
4. **Test Accounts**: Pre-configured testnet accounts listed in submission notes
5. **Demo Credentials**: 
   - Test Hedera Account ID: `0.0.xxxxxxx` (provided separately)
   - Test API Key: `ri_test_xxxxxxxxxxxx` (provided separately)

**Access Method**: Credentials are shared securely via DoraHacks submission platform text field, not in public repository.

---

## 📦 Code Quality & Auditability

### Code Standards

- **Python**: Following PEP 8, type hints, async/await patterns
- **TypeScript**: Strict mode, React best practices
- **Linting**: ESLint (frontend), Black/isort (backend)
- **Testing**: Pytest for backend, Jest for frontend (tests in `tests/` directory)

### Key Files for Judges to Review

**Backend Core Logic:**
- `api/api/services/hedera_service.py` - Hedera transaction execution
- `api/api/services/account_service.py` - Account management
- `api/api/services/transfer_service.py` - Transfer processing
- `api/api/core/config.py` - Configuration management

**Frontend Core Logic:**
- `frontend/src/lib/api.ts` - API client implementation
- `frontend/src/pages/Accounts.tsx` - Account management UI
- `frontend/src/pages/Transfers.tsx` - Transfer interface

### Inline Comments

Complex logic is documented with inline comments explaining:
- Hedera SDK usage patterns
- Transaction fee calculations
- Error handling strategies
- Network fallback mechanisms

---

## 🌐 AWS Deployment via GitHub Actions

### Prerequisites

1. **AWS Account** with credits
2. **GitHub Repository** (public)
3. **AWS Services**:
   - S3 bucket for frontend
   - CloudFront distribution (optional)
   - ECR repository for backend Docker images
   - ECS cluster or Elastic Beanstalk for backend

### Setup GitHub Secrets

Add these secrets in GitHub repository settings → Secrets:

```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=rowell-infra-frontend
CLOUDFRONT_DISTRIBUTION_ID=your-distribution-id (optional)
ECR_REPOSITORY_NAME=rowell-infra-api
ECS_CLUSTER_NAME=rowell-infra-cluster (optional)
ECS_SERVICE_NAME=rowell-infra-service (optional)
VITE_API_URL=https://api.your-domain.com
```

### Deployment Workflows

**Frontend Deployment** (`.github/workflows/deploy-frontend.yml`):
- Triggers on push to `main` branch when `frontend/` changes
- Builds React app with `npm run build`
- Deploys to S3 bucket
- Invalidates CloudFront cache

**Backend Deployment** (`.github/workflows/deploy-backend.yml`):
- Triggers on push to `main` branch when `api/` changes
- Builds Docker image
- Pushes to ECR
- Deploys to ECS or Elastic Beanstalk

### Manual Deployment

If you prefer manual deployment:

```bash
# Frontend
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name/

# Backend
cd api
docker build -t rowell-infra-api .
docker tag rowell-infra-api:latest your-ecr-url/rowell-infra-api:latest
docker push your-ecr-url/rowell-infra-api:latest
```

---

## 📚 Additional Resources

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Hedera Docs**: https://docs.hedera.com
- **Hedera Portal**: https://portal.hedera.com
- **Stellar Docs**: https://developers.stellar.org

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
