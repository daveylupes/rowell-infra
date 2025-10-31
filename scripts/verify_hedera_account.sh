#!/bin/bash
# Verify if a Hedera account exists on the blockchain

ACCOUNT_ID=$1
NETWORK=${2:-testnet}

if [ -z "$ACCOUNT_ID" ]; then
  echo "Usage: $0 <account_id> [testnet|mainnet]"
  echo "Example: $0 0.0.740063450 testnet"
  exit 1
fi

if [ "$NETWORK" = "testnet" ]; then
  MIRROR_URL="https://testnet.mirrornode.hedera.com"
  EXPLORER_URL="https://hashscan.io/testnet/account"
else
  MIRROR_URL="https://mainnet-public.mirrornode.hedera.com"
  EXPLORER_URL="https://hashscan.io/mainnet/account"
fi

echo "🔍 Checking account $ACCOUNT_ID on Hedera $NETWORK..."
echo ""

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$MIRROR_URL/api/v1/accounts/$ACCOUNT_ID")

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Account EXISTS on Hedera blockchain (REAL ACCOUNT)"
  echo ""
  echo "📊 Account Details:"
  curl -s "$MIRROR_URL/api/v1/accounts/$ACCOUNT_ID" | python3 -m json.tool 2>/dev/null || curl -s "$MIRROR_URL/api/v1/accounts/$ACCOUNT_ID"
  echo ""
  echo "🔗 View on Explorer:"
  echo "   $EXPLORER_URL/$ACCOUNT_ID"
elif [ "$HTTP_CODE" = "404" ]; then
  echo "❌ Account NOT FOUND on blockchain (MOCK ACCOUNT)"
  echo ""
  echo "💡 This account was created in mock mode."
  echo "   To create real accounts, configure Hedera credentials:"
  echo "   1. Get credentials from https://portal.hedera.com/"
  echo "   2. Set HEDERA_TESTNET_OPERATOR_ID and HEDERA_TESTNET_OPERATOR_KEY"
  echo ""
  echo "🔗 Try viewing anyway (will show 404):"
  echo "   $EXPLORER_URL/$ACCOUNT_ID"
else
  echo "⚠️  Error checking account: HTTP $HTTP_CODE"
  echo "   This might indicate a network issue or invalid account format."
fi

