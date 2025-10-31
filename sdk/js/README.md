# Rowell Infra JavaScript SDK

[![npm version](https://badge.fury.io/js/%40rowell-infra%2Fsdk.svg)](https://badge.fury.io/js/%40rowell-infra%2Fsdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

The official JavaScript/TypeScript SDK for Rowell Infra - Alchemy for Africa: Stellar + Hedera APIs & Analytics.

## Features

- ✅ **Full API Coverage** - Complete access to all Rowell Infra API endpoints
- ✅ **TypeScript Support** - Full type definitions for better development experience
- ✅ **Automatic Retries** - Built-in exponential backoff retry logic
- ✅ **Error Handling** - Comprehensive error handling with detailed error information
- ✅ **Rate Limiting** - Automatic handling of rate limits with retry logic
- ✅ **Request/Response Logging** - Configurable logging for debugging
- ✅ **Promise-based** - Modern async/await API
- ✅ **Tree Shaking** - Optimized bundle size with tree shaking support

## Installation

```bash
npm install @rowell-infra/sdk
```

Or with yarn:

```bash
yarn add @rowell-infra/sdk
```

## Quick Start

```typescript
import { RowellClient } from '@rowell-infra/sdk';

// Initialize the client
const client = new RowellClient({
  baseUrl: 'https://api.rowellinfra.com',
  apiKey: 'your-api-key-here',
  timeout: 30000,
  enableLogging: true
});

// Create an account
const account = await client.accounts.create({
  network: 'stellar',
  environment: 'testnet',
  account_type: 'individual',
  country_code: 'NG'
});

console.log('Created account:', account);

// Create a transfer
const transfer = await client.transfers.create({
  from_account: account.id,
  to_account: 'recipient-account-id',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet',
  memo: 'Payment for services'
});

console.log('Created transfer:', transfer);
```

## Configuration

### Basic Configuration

```typescript
const client = new RowellClient({
  baseUrl: 'https://api.rowellinfra.com', // Required
  apiKey: 'your-api-key-here',           // Optional
  timeout: 30000,                        // Optional (default: 30000ms)
  headers: {                             // Optional
    'Custom-Header': 'custom-value'
  },
  enableLogging: true                    // Optional (default: true)
});
```

### Retry Configuration

```typescript
const client = new RowellClient({
  baseUrl: 'https://api.rowellinfra.com',
  apiKey: 'your-api-key-here',
  retry: {
    maxRetries: 3,        // Maximum number of retry attempts
    baseDelay: 1000,      // Base delay in milliseconds
    maxDelay: 30000,      // Maximum delay in milliseconds
    backoffFactor: 2,     // Exponential backoff factor
    retryCondition: (error) => {
      // Custom retry condition
      return error.response?.status >= 500;
    }
  }
});
```

## API Services

### Account Service

```typescript
// Create an account
const account = await client.accounts.create({
  network: 'stellar',
  environment: 'testnet',
  account_type: 'individual',
  country_code: 'NG'
});

// List accounts with filtering
const accounts = await client.accounts.list({
  network: 'stellar',
  environment: 'testnet',
  limit: 10,
  offset: 0
});

// Get account details
const accountDetails = await client.accounts.getDetails('account-id', {
  includeBalances: true,
  includeTransactions: true,
  includeCompliance: true
});

// Get account balances
const balances = await client.accounts.getBalances('account-id');

// Search accounts
const searchResults = await client.accounts.search({
  query: 'search-term',
  network: 'stellar',
  country_code: 'NG'
});
```

### Transfer Service

```typescript
// Create a transfer
const transfer = await client.transfers.create({
  from_account: 'from-account-id',
  to_account: 'to-account-id',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet',
  memo: 'Payment for services'
});

// Get transfer status
const status = await client.transfers.getStatus('transfer-id', {
  includeEvents: true,
  includeFees: true,
  includeCompliance: true
});

// List transfers
const transfers = await client.transfers.list({
  from_account: 'account-id',
  network: 'stellar',
  status: 'success',
  limit: 20
});

// Estimate fees
const feeEstimate = await client.transfers.estimateFees({
  from_account: 'from-account-id',
  to_account: 'to-account-id',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet'
});
```

### Analytics Service

```typescript
// Get dashboard analytics
const dashboard = await client.analytics.getDashboard({
  period_type: 'monthly',
  start_date: '2024-01-01',
  end_date: '2024-01-31'
});

// Get remittance flows
const remittanceFlows = await client.analytics.getRemittanceFlows({
  from_country: 'NG',
  to_country: 'KE',
  period_type: 'daily',
  limit: 50
});

// Get stablecoin adoption
const stablecoinAdoption = await client.analytics.getStablecoinAdoption({
  asset_code: 'USDC',
  country_code: 'NG',
  period_type: 'monthly'
});

// Get merchant activity
const merchantActivity = await client.analytics.getMerchantActivity({
  merchant_type: 'fintech',
  country_code: 'NG',
  period_type: 'weekly'
});

// Get network metrics
const networkMetrics = await client.analytics.getNetworkMetrics({
  network: 'stellar',
  environment: 'testnet',
  period_type: 'daily'
});
```

### Compliance Service

```typescript
// Initiate KYC verification
const kycVerification = await client.compliance.initiateKYC({
  account_id: 'account-id',
  network: 'stellar',
  verification_type: 'individual',
  first_name: 'John',
  last_name: 'Doe',
  date_of_birth: '1990-01-01',
  nationality: 'NG',
  document_type: 'bvn',
  bvn: '12345678901'
});

// Get KYC status
const kycStatus = await client.compliance.getKYCStatus('verification-id');

// List compliance flags
const flags = await client.compliance.listFlags({
  entity_type: 'transaction',
  flag_severity: 'high',
  limit: 20
});

// Create compliance flag
const flag = await client.compliance.createFlag({
  entity_type: 'transaction',
  entity_id: 'transaction-id',
  network: 'stellar',
  flag_type: 'aml',
  flag_severity: 'medium',
  flag_reason: 'Unusual transaction pattern'
});

// Get compliance reports
const reports = await client.compliance.getComplianceReports({
  report_type: 'monthly',
  country_code: 'NG'
});
```

## Error Handling

The SDK provides comprehensive error handling with detailed error information:

```typescript
import { RowellError } from '@rowell-infra/sdk';

try {
  const account = await client.accounts.create({
    network: 'stellar',
    environment: 'testnet',
    account_type: 'individual'
  });
} catch (error) {
  if (error instanceof RowellError) {
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    console.error('Error details:', error.details);
    console.error('Timestamp:', error.timestamp);
  }
}
```

### Error Types

- **ValidationError**: Invalid request parameters
- **AuthenticationError**: Invalid or missing API key
- **AuthorizationError**: Insufficient permissions
- **NotFoundError**: Resource not found
- **RateLimitError**: Rate limit exceeded
- **NetworkError**: Network connectivity issues
- **ServerError**: Server-side errors

## Retry Logic

The SDK automatically retries failed requests with exponential backoff:

```typescript
const client = new RowellClient({
  baseUrl: 'https://api.rowellinfra.com',
  apiKey: 'your-api-key-here',
  retry: {
    maxRetries: 3,           // Retry up to 3 times
    baseDelay: 1000,         // Start with 1 second delay
    maxDelay: 30000,         // Maximum 30 second delay
    backoffFactor: 2,        // Double delay each retry
    retryCondition: (error) => {
      // Retry on server errors and rate limits
      return error.response?.status >= 500 || error.response?.status === 429;
    }
  }
});
```

## Logging

Enable or disable request/response logging:

```typescript
// Enable logging (default)
client.setLogging(true);

// Disable logging
client.setLogging(false);
```

## TypeScript Support

The SDK is written in TypeScript and provides full type definitions:

```typescript
import {
  RowellClient,
  Account,
  Transfer,
  KYCVerification,
  ComplianceFlag,
  Network,
  Environment,
  AccountType
} from '@rowell-infra/sdk';

const network: Network = 'stellar';
const environment: Environment = 'testnet';
const accountType: AccountType = 'individual';

const account: Account = await client.accounts.create({
  network,
  environment,
  account_type: accountType
});
```

## Examples

### Complete Transfer Flow

```typescript
import { RowellClient } from '@rowell-infra/sdk';

const client = new RowellClient({
  baseUrl: 'https://api.rowellinfra.com',
  apiKey: 'your-api-key-here'
});

async function sendPayment(fromAccountId: string, toAccountId: string, amount: string) {
  try {
    // 1. Check sender account balance
    const balances = await client.accounts.getBalances(fromAccountId);
    const usdcBalance = balances.find(b => b.asset_code === 'USDC');
    
    if (!usdcBalance || parseFloat(usdcBalance.balance) < parseFloat(amount)) {
      throw new Error('Insufficient balance');
    }

    // 2. Estimate fees
    const feeEstimate = await client.transfers.estimateFees({
      from_account: fromAccountId,
      to_account: toAccountId,
      asset_code: 'USDC',
      amount,
      network: 'stellar',
      environment: 'testnet'
    });

    console.log('Estimated fees:', feeEstimate);

    // 3. Create transfer
    const transfer = await client.transfers.create({
      from_account: fromAccountId,
      to_account: toAccountId,
      asset_code: 'USDC',
      amount,
      network: 'stellar',
      environment: 'testnet',
      memo: 'Payment via Rowell SDK'
    });

    console.log('Transfer created:', transfer.id);

    // 4. Monitor transfer status
    const checkStatus = async () => {
      const status = await client.transfers.getStatus(transfer.id, {
        includeEvents: true,
        includeFees: true,
        includeCompliance: true
      });

      console.log('Transfer status:', status.status);

      if (status.status === 'pending') {
        setTimeout(checkStatus, 5000); // Check again in 5 seconds
      } else if (status.status === 'success') {
        console.log('Transfer completed successfully!');
      } else {
        console.error('Transfer failed:', status);
      }
    };

    checkStatus();

  } catch (error) {
    console.error('Transfer failed:', error);
  }
}
```

### Analytics Dashboard

```typescript
async function buildAnalyticsDashboard() {
  try {
    // Get dashboard overview
    const dashboard = await client.analytics.getDashboard({
      period_type: 'monthly'
    });

    console.log('Total accounts:', dashboard.total_accounts);
    console.log('Total volume:', dashboard.total_transaction_volume_usd);

    // Get remittance flows for Africa
    const remittanceFlows = await client.analytics.getRemittanceFlows({
      from_region: 'Africa',
      to_region: 'Africa',
      period_type: 'daily',
      limit: 100
    });

    console.log('Top remittance corridors:', remittanceFlows.analytics.top_corridors);

    // Get stablecoin adoption
    const stablecoinAdoption = await client.analytics.getStablecoinAdoption({
      period_type: 'monthly'
    });

    console.log('Stablecoin adoption trends:', stablecoinAdoption.analytics.adoption_trends);

    // Get network metrics
    const networkMetrics = await client.analytics.getNetworkMetrics({
      period_type: 'daily'
    });

    console.log('Network performance:', networkMetrics.analytics.summary);

  } catch (error) {
    console.error('Analytics error:', error);
  }
}
```

## Development

### Building the SDK

```bash
npm run build
```

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Formatting

```bash
npm run format
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://docs.rowellinfra.com](https://docs.rowellinfra.com)
- **Issues**: [GitHub Issues](https://github.com/rowell-infra/rowell-infra/issues)
- **Email**: [support@rowellinfra.com](mailto:support@rowellinfra.com)

## Changelog

### v1.0.0
- Initial release
- Full API coverage
- TypeScript support
- Automatic retries
- Comprehensive error handling
- Rate limiting support
- Request/response logging
