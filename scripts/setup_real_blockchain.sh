#!/bin/bash
# Setup script to enable real Hedera blockchain accounts

set -e

echo "🚀 Setting up Real Blockchain Integration"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Java
echo "1️⃣  Checking Java installation..."
if java -version 2>&1 | grep -q "version"; then
    JAVA_VERSION=$(java -version 2>&1 | head -1 | awk -F '"' '{print $2}')
    echo -e "${GREEN}✅ Java installed: $JAVA_VERSION${NC}"
    
    # Check JAVA_HOME
    if [ -z "$JAVA_HOME" ]; then
        echo -e "${YELLOW}⚠️  JAVA_HOME not set${NC}"
        JAVA_HOME=$(readlink -f $(which java) | sed "s:bin/java::")
        echo "   Detected JAVA_HOME: $JAVA_HOME"
        echo "   Add to your ~/.bashrc or ~/.zshrc:"
        echo "   export JAVA_HOME=$JAVA_HOME"
    else
        echo -e "${GREEN}✅ JAVA_HOME set: $JAVA_HOME${NC}"
    fi
else
    echo -e "${RED}❌ Java not found${NC}"
    echo "   Install Java 11+: sudo apt install openjdk-11-jdk"
    exit 1
fi

# Check Python
echo ""
echo "2️⃣  Checking Python installation..."
if python3 --version &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 not found${NC}"
    exit 1
fi

# Check Hedera SDK
echo ""
echo "3️⃣  Checking Hedera SDK..."
cd api
if python3 -c "import hedera" 2>/dev/null; then
    echo -e "${GREEN}✅ Hedera SDK installed${NC}"
else
    echo -e "${YELLOW}⚠️  Hedera SDK not working${NC}"
    echo "   Installing Hedera SDK..."
    pip install --force-reinstall hedera-sdk-py || pip3 install --force-reinstall hedera-sdk-py
    if python3 -c "import hedera" 2>/dev/null; then
        echo -e "${GREEN}✅ Hedera SDK installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install Hedera SDK${NC}"
        echo "   Make sure JAVA_HOME is set correctly"
        exit 1
    fi
fi

# Check environment variables
echo ""
echo "4️⃣  Checking Hedera credentials..."
if [ -f .env ]; then
    if grep -q "HEDERA_TESTNET_OPERATOR_ID" .env && grep -q "HEDERA_TESTNET_OPERATOR_KEY" .env; then
        echo -e "${GREEN}✅ Credentials found in .env file${NC}"
        
        # Source .env to check values
        source .env 2>/dev/null || true
        
        if [ -n "$HEDERA_TESTNET_OPERATOR_ID" ] && [ -n "$HEDERA_TESTNET_OPERATOR_KEY" ]; then
            echo -e "${GREEN}✅ Credentials are set${NC}"
            echo "   Operator ID: $HEDERA_TESTNET_OPERATOR_ID"
            echo "   Operator Key: ${HEDERA_TESTNET_OPERATOR_KEY:0:20}..."
        else
            echo -e "${YELLOW}⚠️  Credentials in .env but values are empty${NC}"
            echo "   Please add:"
            echo "   HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx"
            echo "   HEDERA_TESTNET_OPERATOR_KEY=302e..."
        fi
    else
        echo -e "${YELLOW}⚠️  Credentials not found in .env${NC}"
        echo "   Add these to your .env file:"
        echo "   HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx"
        echo "   HEDERA_TESTNET_OPERATOR_KEY=302e..."
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "   Create .env file with:"
    echo "   HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx"
    echo "   HEDERA_TESTNET_OPERATOR_KEY=302e..."
fi

# Instructions
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get Hedera Testnet Credentials:"
echo "   - Visit: https://portal.hedera.com/"
echo "   - Create account → Developer → Testnet Access"
echo "   - Copy Account ID and Private Key"
echo ""
echo "2. Add to .env file:"
echo "   HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx"
echo "   HEDERA_TESTNET_OPERATOR_KEY=302e..."
echo ""
echo "3. Fund your operator account:"
echo "   - Get testnet HBAR from Hedera Portal (FREE)"
echo "   - Recommended: 100+ HBAR for testing"
echo ""
echo "4. Restart backend and test:"
echo "   python3 main.py"
echo ""
echo "5. Verify real account creation:"
echo "   curl -X POST http://localhost:8000/api/v1/accounts/create \\"
echo "     -H 'Authorization: Bearer YOUR_API_KEY' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"network\":\"hedera\",\"environment\":\"testnet\",\"account_type\":\"user\",\"country_code\":\"NG\"}'"
echo ""
echo -e "${GREEN}✅ Setup check complete!${NC}"
cd ..

