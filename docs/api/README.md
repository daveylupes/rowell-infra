# 📡 Rowell Infra API Reference

> **Complete API Documentation for African Fintech Infrastructure**

The Rowell Infra API provides a unified interface for building cross-border payment applications using Stellar and Hedera networks. This reference covers all endpoints, request/response formats, and authentication.

## 🔗 **Base URLs**

### **Development**
```
http://localhost:8000
```

### **Production**
```
https://api.rowell-infra.com
```

## 🔐 **Authentication**

All API requests require authentication using API keys:

```bash
Authorization: Bearer your_api_key_here
```

### **Getting API Keys**

1. **Testnet Keys**: Available immediately after signup
2. **Mainnet Keys**: Require verification and approval
3. **Enterprise Keys**: Contact support for custom limits

## 📋 **API Endpoints Overview**

### **Health & Information**
- **[Health Check](health.md)** - API status and version
- **[API Information](info.md)** - Network details and capabilities

### **Account Management**
- **[Create Account](accounts.md#create-account)** - Create new accounts
- **[List Accounts](accounts.md#list-accounts)** - Get account listings
- **[Account Details](accounts.md#account-details)** - Get account information
- **[Account Balances](accounts.md#account-balances)** - Get balance information

### **Transfer Management**
- **[Create Transfer](transfers.md#create-transfer)** - Create new transfers
- **[Transfer Status](transfers.md#transfer-status)** - Get transfer status
- **[List Transfers](transfers.md#list-transfers)** - Get transfer listings
- **[Transfer Events](transfers.md#transfer-events)** - Get transfer events

### **Analytics**
- **[Remittance Flows](analytics.md#remittance-flows)** - Get remittance analytics
- **[Stablecoin Adoption](analytics.md#stablecoin-adoption)** - Track stablecoin usage
- **[Merchant Activity](analytics.md#merchant-activity)** - Monitor merchant performance
- **[Network Metrics](analytics.md#network-metrics)** - Get network statistics

### **Compliance**
- **[KYC Verification](compliance.md#kyc-verification)** - Identity verification
- **[Compliance Flags](compliance.md#compliance-flags)** - Risk assessment
- **[Sanctions Check](compliance.md#sanctions-check)** - Sanctions screening

## 🚀 **Quick Start**

### **1. Get Your API Key**
```bash
# Test API key (development)
export ROWELL_API_KEY="sk_test_1234567890"
```

### **2. Test the API**
```bash
curl -H "Authorization: Bearer $ROWELL_API_KEY" \
     http://localhost:8000/health
```

### **3. Create Your First Account**
```bash
curl -X POST "http://localhost:8000/api/v1/accounts/create" \
  -H "Authorization: Bearer $ROWELL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "KE"
  }'
```

## 📊 **Response Format**

All API responses follow a consistent format:

### **Success Response**
```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### **Error Response**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "country_code",
      "reason": "Invalid country code"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔄 **Rate Limiting**

API requests are rate limited to ensure fair usage:

- **Free Tier**: 100 requests/minute
- **Pro Tier**: 1,000 requests/minute
- **Enterprise**: Custom limits

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

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
- **Nigeria**: BVN, NIN
- **South Africa**: SA ID Number
- **Ghana**: Ghana Card
- **Kenya**: National ID

## 🔧 **SDKs and Libraries**

### **JavaScript/TypeScript**
```bash
npm install @rowell-infra/sdk
```

### **Python**
```bash
pip install rowell-infra
```

### **Flutter**
```yaml
dependencies:
  rowell_infra: ^1.0.0
```

## 📚 **Additional Resources**

- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI
- **[Postman Collection](postman.md)** - Import into Postman
- **[SDK Documentation](../sdk/README.md)** - SDK usage guides
- **[Webhooks](webhooks.md)** - Event notifications
- **[Error Codes](error-codes.md)** - Complete error reference

## 🆘 **Support**

- **📧 Email**: developers@rowell-infra.com
- **💬 Discord**: [discord.gg/rowell-infra](https://discord.gg/rowell-infra)
- **🐛 Issues**: [GitHub Issues](https://github.com/rowell-infra/rowell-infra/issues)
- **📖 FAQ**: [Frequently Asked Questions](../support/faq.md)

---

*This API reference is updated with each release. Last updated: January 2025*
