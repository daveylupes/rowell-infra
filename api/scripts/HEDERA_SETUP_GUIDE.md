# Hedera Integration Setup Guide

This guide explains how to set up real Hedera testnet integration for the hackathon demo.

## Prerequisites

### 1. Java 17+ Installation

Hedera SDK requires Java 17 or higher:

```bash
# Check Java version
java -version

# If not installed, install Java 17:
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install openjdk-17-jdk

# macOS:
brew install openjdk@17
```

### 2. Hedera Testnet Account

You need a Hedera testnet account to serve as the "operator" for transactions:

1. Visit: https://portal.hedera.com/
2. Create a testnet account (free)
3. Save your **Account ID** and **Private Key**

## Configuration

### Option 1: Environment Variables (Recommended)

Set these environment variables:

```bash
export HEDERA_TESTNET_OPERATOR_ID="0.0.1234567"
export HEDERA_TESTNET_OPERATOR_KEY="302e0201..."  # Your private key
```

### Option 2: .env File

Add to `api/.env`:

```env
HEDERA_TESTNET_OPERATOR_ID=0.0.1234567
HEDERA_TESTNET_OPERATOR_KEY=302e0201...
```

## Installation

### 1. Install Hedera SDK

```bash
cd api
source venv/bin/activate
pip install hedera-sdk-py
```

### 2. Verify Installation

```bash
python -c "from hedera import Client; print('Hedera SDK installed successfully')"
```

## Validation

Run the validation script to test integration:

```bash
cd api
source venv/bin/activate
python scripts/validate_hedera_integration.py
```

The script tests:
- ✅ Account creation
- ✅ Account information retrieval
- ✅ Balance queries
- ✅ Mirror Node API connectivity
- ⚠️ Payment transactions (requires operator)

## Demo Mode vs Real Mode

### Demo Mode (Fallback)

If Hedera SDK is not installed or operator is not configured:
- ✅ Read operations work (via Mirror Node API)
- ✅ Account creation returns mock accounts
- ⚠️ Transactions return mock responses

**This is OK for hackathon demo if you only need to show the UI flow.**

### Real Mode (Full Integration)

With Hedera SDK and operator configured:
- ✅ Real account creation on testnet
- ✅ Real transactions on testnet
- ✅ Real balance queries
- ✅ Full blockchain integration

**This is better for hackathon demo to show real blockchain integration.**

## Troubleshooting

### "Hedera SDK not available"

**Solution:** Install hedera-sdk-py and Java 17+

```bash
pip install hedera-sdk-py
# Install Java 17+
```

### "Hedera operator not configured"

**Solution:** Set environment variables:

```bash
export HEDERA_TESTNET_OPERATOR_ID="0.0.1234567"
export HEDERA_TESTNET_OPERATOR_KEY="your_private_key"
```

### "Java not found"

**Solution:** Install Java 17+ and ensure it's in PATH

### Mirror Node API Works But SDK Doesn't

**This is OK!** Mirror Node API works without SDK. You can:
- ✅ Show account info
- ✅ Show balances
- ✅ Query transactions
- ⚠️ Create accounts/transactions (requires SDK)

## Hackathon Demo Recommendations

1. **Minimal Setup:** Use Mirror Node API only (no SDK needed)
   - Pro: Quick setup, works immediately
   - Con: Can't create real transactions

2. **Full Setup:** Install SDK + Configure Operator
   - Pro: Real transactions, impressive demo
   - Con: Requires Java + Hedera account setup

3. **Hybrid:** SDK for demo, Mirror Node for production
   - Use SDK during hackathon presentation
   - Fall back to Mirror Node if SDK unavailable

## Testnet Account Funding

Hedera testnet accounts are automatically funded with test HBAR. If you need more:

1. Visit: https://portal.hedera.com/
2. Request testnet tokens (free)
3. Transfer to your operator account

## Security Notes

⚠️ **Never commit private keys to version control!**

- Use environment variables
- Add `.env` to `.gitignore`
- Use secret management in production

## Support

For Hedera-specific issues:
- Documentation: https://docs.hedera.com/
- Discord: https://hedera.com/discord
- Portal: https://portal.hedera.com/

