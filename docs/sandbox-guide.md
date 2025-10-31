# Rowell Infra Sandbox Environment Guide

## Overview

The Rowell Infra Sandbox Environment provides a safe, isolated testing environment for developers to build and test their integrations without affecting real accounts or transactions. The sandbox includes comprehensive mock data generation, rate limiting testing, and pre-built test scenarios.

## Getting Started

### 1. API Key Setup

First, you'll need a sandbox API key. Contact support to get your sandbox credentials.

```bash
# Set your sandbox API key
export ROWELL_SANDBOX_API_KEY="your-sandbox-api-key"
```

### 2. Base URL

Use the sandbox base URL for all your requests:

```bash
# Sandbox environment
https://api-sandbox.rowellinfra.com
```

### 3. SDK Configuration

Configure your SDK to use the sandbox environment:

```javascript
// JavaScript SDK
import { RowellClient } from '@rowell-infra/sdk';

const client = new RowellClient({
  baseUrl: 'https://api-sandbox.rowellinfra.com',
  apiKey: 'your-sandbox-api-key',
  enableLogging: true  // Enable for debugging
});
```

```python
# Python SDK
from rowell_infra import RowellClient

client = RowellClient(
    base_url='https://api-sandbox.rowellinfra.com',
    api_key='your-sandbox-api-key'
)
```

## Sandbox Features

### Mock Data Generation

The sandbox provides comprehensive mock data generation for all major data types:

#### Accounts
Generate test accounts with realistic data:

```bash
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/accounts/generate?count=10" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### Transactions
Generate test transactions between accounts:

```bash
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/transactions/generate?account_ids=acc1&account_ids=acc2&count=50" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### Analytics Data
Generate comprehensive analytics data:

```bash
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/analytics/generate" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### Compliance Data
Generate KYC verifications and compliance flags:

```bash
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/compliance/generate?account_ids=acc1&entity_ids=entity1&kyc_count=20&flag_count=15" \
  -H "X-API-Key: your-sandbox-api-key"
```

### Rate Limiting

The sandbox environment includes rate limiting to help you test your application's handling of rate limits:

#### Rate Limits
- **Requests per minute**: 1,000
- **Requests per hour**: 60,000
- **Requests per day**: 1,000,000
- **Burst limit**: 1,500

#### Rate Limit Headers
Monitor these headers in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
Retry-After: 60  # Only on 429 responses
```

#### Rate Limit Testing
Test rate limiting behavior:

```bash
# Generate many requests quickly to trigger rate limits
for i in {1..1200}; do
  curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/sandbox/stats" \
    -H "X-API-Key: your-sandbox-api-key" &
done
wait
```

### Test Scenarios

The sandbox provides pre-built test scenarios to help you test different aspects of your integration:

#### 1. Basic Integration Test
**Duration**: 5-10 minutes

Test basic account creation and transfer functionality:

```bash
# 1. Generate test accounts
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/accounts/generate?count=5" \
  -H "X-API-Key: your-sandbox-api-key"

# 2. Create a transfer between accounts
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/transfers" \
  -H "X-API-Key: your-sandbox-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "SB123456",
    "to_account": "SB789012",
    "asset_code": "USDC",
    "amount": "100.00",
    "network": "stellar",
    "environment": "testnet"
  }'

# 3. Check transfer status
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/transfers/{transfer_id}/status" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### 2. Compliance Testing
**Duration**: 10-15 minutes

Test KYC verification and compliance flagging:

```bash
# 1. Generate KYC verifications
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/compliance/generate?kyc_count=10" \
  -H "X-API-Key: your-sandbox-api-key"

# 2. Check KYC status
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/compliance/verify-id/{verification_id}" \
  -H "X-API-Key: your-sandbox-api-key"

# 3. Generate compliance flags
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/compliance/generate?flag_count=5" \
  -H "X-API-Key: your-sandbox-api-key"

# 4. List compliance flags
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/compliance/flags" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### 3. Analytics Testing
**Duration**: 15-20 minutes

Test analytics and reporting functionality:

```bash
# 1. Generate analytics data
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/analytics/generate" \
  -H "X-API-Key: your-sandbox-api-key"

# 2. Get dashboard analytics
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/analytics/dashboard" \
  -H "X-API-Key: your-sandbox-api-key"

# 3. Get remittance flows
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/analytics/remittance-flows?from_country=NG&to_country=KE" \
  -H "X-API-Key: your-sandbox-api-key"

# 4. Get stablecoin adoption
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/analytics/stablecoin-adoption?asset_code=USDC" \
  -H "X-API-Key: your-sandbox-api-key"
```

#### 4. Stress Testing
**Duration**: 20-30 minutes

Test system performance under load:

```bash
# 1. Generate large volume of accounts
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/accounts/generate?count=100" \
  -H "X-API-Key: your-sandbox-api-key"

# 2. Generate many transactions
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/transactions/generate?count=1000" \
  -H "X-API-Key: your-sandbox-api-key"

# 3. Test concurrent requests
for i in {1..100}; do
  curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/sandbox/stats" \
    -H "X-API-Key: your-sandbox-api-key" &
done
wait
```

#### 5. Error Handling Testing
**Duration**: 10-15 minutes

Test error scenarios and edge cases:

```bash
# 1. Test invalid API key
curl -X GET "https://api-sandbox.rowellinfra.com/api/v1/sandbox/stats" \
  -H "X-API-Key: invalid-key"

# 2. Test malformed requests
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/transfers" \
  -H "X-API-Key: your-sandbox-api-key" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# 3. Test rate limit scenarios
# (Use the rate limit testing script above)

# 4. Test invalid parameters
curl -X POST "https://api-sandbox.rowellinfra.com/api/v1/sandbox/accounts/generate?count=0" \
  -H "X-API-Key: your-sandbox-api-key"
```

## API Endpoints

### Sandbox Management

#### Get Sandbox Statistics
```http
GET /api/v1/sandbox/stats
```

Returns current sandbox environment statistics.

#### Reset Sandbox Data
```http
POST /api/v1/sandbox/reset
```

Resets all sandbox data to initial state.

#### Get Test Scenarios
```http
GET /api/v1/sandbox/scenarios
```

Returns available test scenarios and usage instructions.

#### Get Rate Limits
```http
GET /api/v1/sandbox/rate-limits
```

Returns sandbox rate limiting information and testing guidelines.

### Mock Data Generation

#### Generate Mock Accounts
```http
POST /api/v1/sandbox/accounts/generate?count={count}
```

**Parameters:**
- `count` (integer): Number of accounts to generate (1-100)

#### Generate Mock Transactions
```http
POST /api/v1/sandbox/transactions/generate?account_ids={ids}&count={count}
```

**Parameters:**
- `account_ids` (array): List of account IDs to generate transactions for
- `count` (integer): Number of transactions to generate (1-1000)

#### Generate Mock Analytics
```http
POST /api/v1/sandbox/analytics/generate
```

Generates comprehensive analytics data including remittance flows, stablecoin adoption, merchant activity, and network metrics.

#### Generate Mock Compliance Data
```http
POST /api/v1/sandbox/compliance/generate?account_ids={ids}&entity_ids={ids}&kyc_count={count}&flag_count={count}
```

**Parameters:**
- `account_ids` (array): List of account IDs for KYC verifications
- `entity_ids` (array): List of entity IDs for compliance flags
- `kyc_count` (integer): Number of KYC verifications to generate (1-100)
- `flag_count` (integer): Number of compliance flags to generate (1-100)

## Best Practices

### 1. Data Management
- **Reset regularly**: Use the reset endpoint to clean up test data
- **Use realistic data**: The mock data generator creates realistic test scenarios
- **Test edge cases**: Generate data with various states (active/inactive, verified/unverified)

### 2. Rate Limiting
- **Implement retry logic**: Handle 429 responses with exponential backoff
- **Monitor headers**: Track rate limit usage using response headers
- **Test limits**: Intentionally hit rate limits to test your error handling

### 3. Error Handling
- **Test all error scenarios**: Invalid API keys, malformed requests, server errors
- **Implement proper logging**: Log all errors for debugging
- **Use appropriate HTTP status codes**: Handle different error types correctly

### 4. Testing Workflow
1. **Start fresh**: Reset sandbox data before starting tests
2. **Generate data**: Create the mock data you need for your tests
3. **Run scenarios**: Follow the pre-built test scenarios
4. **Clean up**: Reset data when finished testing

### 5. SDK Usage
- **Use sandbox configuration**: Always use sandbox URLs and API keys
- **Enable logging**: Turn on request/response logging for debugging
- **Test retry logic**: Verify your SDK handles retries correctly

## Monitoring and Debugging

### Request Logging
Enable request logging in your SDK:

```javascript
const client = new RowellClient({
  baseUrl: 'https://api-sandbox.rowellinfra.com',
  apiKey: 'your-sandbox-api-key',
  enableLogging: true
});
```

### Response Headers
Monitor these headers for debugging:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-Request-ID: req_123456789
```

### Error Responses
Sandbox errors include detailed information:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "count",
      "reason": "Must be between 1 and 100"
    },
    "timestamp": "2024-01-27T12:00:00Z"
  }
}
```

## Support

### Documentation
- **API Reference**: https://docs.rowellinfra.com/api
- **SDK Documentation**: https://docs.rowellinfra.com/sdk
- **Interactive API**: https://api-sandbox.rowellinfra.com/docs

### Getting Help
- **Email**: sandbox-support@rowellinfra.com
- **Slack**: #sandbox-support
- **GitHub Issues**: https://github.com/rowell-infra/rowell-infra/issues

### Common Issues

#### 1. Rate Limit Errors
**Problem**: Getting 429 responses
**Solution**: Implement exponential backoff retry logic

#### 2. Authentication Errors
**Problem**: Getting 401 responses
**Solution**: Verify your API key and headers

#### 3. Data Not Found
**Problem**: Getting 404 responses
**Solution**: Generate mock data first using sandbox endpoints

#### 4. Validation Errors
**Problem**: Getting 422 responses
**Solution**: Check request parameters and data types

## Migration to Production

When you're ready to move to production:

1. **Update base URL**: Change from sandbox to production URL
2. **Get production API key**: Request production credentials
3. **Test with real data**: Verify all functionality works with real data
4. **Update rate limits**: Adjust for production rate limits
5. **Enable monitoring**: Set up production monitoring and alerting

### Production URLs
- **API**: https://api.rowellinfra.com
- **Documentation**: https://docs.rowellinfra.com
- **Support**: support@rowellinfra.com
