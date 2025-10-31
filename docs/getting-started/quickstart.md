# 🚀 Rowell Infra Quickstart Guide

Welcome to **Rowell Infra** - Alchemy for Africa! This guide will help you get started with building African fintech applications using Stellar and Hedera networks.

## ⚡ **5-Minute Setup**

### **Prerequisites**
- Docker & Docker Compose
- Git
- curl (for testing)

### **1. Clone and Start**
```bash
git clone https://github.com/rowell-infra/rowell-infra.git
cd rowell-infra
docker-compose up -d
```

### **2. Verify It's Working**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### **3. Access API Documentation**
Open your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

🎉 **You're ready to start building!**

---

## 📚 **Core Concepts**

### **Networks & Environments**

Rowell Infra supports both **Stellar** and **Hedera** networks:

- **Stellar**: Fast, low-cost payments with built-in compliance
- **Hedera**: Enterprise-grade DLT with predictable fees
- **Testnet**: Safe environment for development
- **Mainnet**: Production environment

### **Account Types**

- **User**: Individual customers
- **Merchant**: Businesses accepting payments
- **Anchor**: Financial institutions
- **NGO**: Non-profit organizations

### **Key Features**

- **Unified API**: Single interface for both Stellar and Hedera
- **Analytics**: Track remittance flows and stablecoin adoption
- **Compliance**: Built-in KYC and AML tools
- **Real-time**: WebSocket subscriptions for live updates

---

## 💡 **Your First API Call**

### **Create an Account**

```bash
curl -X POST "http://localhost:8000/api/v1/accounts/create" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "KE"
  }'
```

### **Create a Transfer**

```bash
curl -X POST "http://localhost:8000/api/v1/transfers/create" \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "your_account_id",
    "to_account": "destination_account_id",
    "asset_code": "XLM",
    "amount": "10.00",
    "network": "stellar",
    "environment": "testnet"
  }'
```

---

## 🌍 **Africa-Specific Features**

### **Supported Countries**

- **KE**: Kenya 🇰🇪
- **NG**: Nigeria 🇳🇬
- **ZA**: South Africa 🇿🇦
- **GH**: Ghana 🇬🇭
- **UG**: Uganda 🇺🇬
- **TZ**: Tanzania 🇹🇿
- **ET**: Ethiopia 🇪🇹
- **EG**: Egypt 🇪🇬

### **Local ID Types**

- **Nigeria**: BVN (Bank Verification Number), NIN (National ID)
- **South Africa**: SA ID Number
- **Ghana**: Ghana Card
- **Kenya**: National ID

---

## 🔧 **Development Workflow**

### **1. Local Development**

Start the Rowell Infra stack locally:

```bash
git clone https://github.com/rowell-infra/rowell-infra.git
cd rowell-infra
docker-compose up -d
```

### **2. API Documentation**

Visit `http://localhost:8000/docs` for interactive API documentation.

### **3. Monitoring**

- **Grafana**: `http://localhost:3000` (admin/admin)
- **Prometheus**: `http://localhost:9090`

### **4. Testing**

```bash
# Test API health
curl http://localhost:8000/health

# Test account creation
curl -X POST http://localhost:8000/api/v1/accounts/create \
  -H "Content-Type: application/json" \
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "KE"
  }'
```

---

## 📊 **Common Use Cases**

### **1. Cross-Border Remittances**

Send money between African countries:

```javascript
const transfer = await client.transfers.create({
  from_account: 'kenya_user_account',
  to_account: 'nigeria_user_account',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet',
  from_country: 'KE',
  to_country: 'NG'
});
```

### **2. Merchant Payments**

Accept payments in your app:

```javascript
// Create merchant account
const merchant = await client.accounts.create({
  network: 'hedera',
  environment: 'testnet',
  account_type: 'merchant',
  country_code: 'ZA'
});

// Process payment
const payment = await client.transfers.create({
  from_account: 'customer_account',
  to_account: merchant.account_id,
  asset_code: 'HBAR',
  amount: '50.00',
  network: 'hedera',
  environment: 'testnet'
});
```

### **3. Analytics Dashboard**

Track your business metrics:

```javascript
// Get remittance flows
const flows = await client.analytics.getRemittanceFlows({
  from_country: 'KE',
  to_country: 'NG',
  period_type: 'monthly'
});

// Get stablecoin adoption
const adoption = await client.analytics.getStablecoinAdoption({
  asset: 'USDC',
  country_code: 'KE'
});
```

### **4. Compliance & KYC**

Verify your users:

```javascript
// Initiate KYC verification
const verification = await client.compliance.verifyId({
  account_id: 'user_account_id',
  network: 'stellar',
  verification_type: 'individual',
  first_name: 'John',
  last_name: 'Doe',
  document_type: 'national_id',
  document_number: '1234567890',
  document_country: 'KE'
});

// Check verification status
const status = await client.compliance.getKYCVerification(verification.verification_id);
```

---

## 🔒 **Security Best Practices**

### **1. API Keys**

- Store API keys in environment variables
- Use different keys for testnet and mainnet
- Rotate keys regularly

### **2. Private Keys**

- Never store private keys in code
- Use hardware wallets for mainnet
- Implement key management solutions

### **3. Compliance**

- Always verify user identity (KYC)
- Monitor transactions for suspicious activity
- Implement proper AML procedures

---

## 🚀 **Next Steps**

1. **Explore the API**: Try the interactive docs at `/docs`
2. **Build a Demo**: Create a simple remittance app
3. **Join the Community**: Connect with other developers
4. **Contribute**: Help improve Rowell Infra

---

## 📞 **Support**

- **Documentation**: [docs.rowell-infra.com](https://docs.rowell-infra.com)
- **API Reference**: [api.rowell-infra.com/docs](https://api.rowell-infra.com/docs)
- **GitHub**: [github.com/rowell-infra/rowell-infra](https://github.com/rowell-infra/rowell-infra)
- **Discord**: [discord.gg/rowell-infra](https://discord.gg/rowell-infra)
- **Email**: [support@rowell-infra.com](mailto:support@rowell-infra.com)

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
