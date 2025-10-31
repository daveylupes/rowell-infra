#!/usr/bin/env python3
"""
Test script to verify Hedera credentials are loaded correctly
"""
import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.core.config import settings
from api.services.hedera_service import HederaService

def main():
    print("🔍 Checking Hedera Configuration\n")
    
    # Check credentials
    has_id = bool(settings.HEDERA_TESTNET_OPERATOR_ID)
    has_key = bool(settings.HEDERA_TESTNET_OPERATOR_KEY)
    
    print(f"Operator ID set: {'✅' if has_id else '❌'}")
    if has_id:
        id_value = settings.HEDERA_TESTNET_OPERATOR_ID
        print(f"  Value: {id_value[:10]}...{id_value[-4:] if len(id_value) > 14 else id_value}")
    else:
        print("  Value: NOT SET")
    
    print(f"\nOperator Key set: {'✅' if has_key else '❌'}")
    if has_key:
        key_value = settings.HEDERA_TESTNET_OPERATOR_KEY
        print(f"  Value: {key_value[:20]}...{key_value[-10:] if len(key_value) > 30 else key_value}")
    else:
        print("  Value: NOT SET")
    
    # Check Hedera SDK
    print("\n📦 Checking Hedera SDK...")
    try:
        from hedera import Client, AccountId, PrivateKey
        print("✅ Hedera SDK installed")
    except ImportError as e:
        print(f"❌ Hedera SDK not available: {e}")
        return
    
    # Test service initialization
    print("\n🔧 Testing HederaService initialization...")
    try:
        service = HederaService(environment="testnet")
        if service.has_operator:
            print("✅ HederaService configured with operator credentials")
            print("✅ REAL accounts can be created!")
        else:
            print("❌ HederaService NOT configured with operator")
            print("⚠️  Accounts will be created in MOCK mode")
            
            if not has_id or not has_key:
                print("\n💡 Solution:")
                print("   1. Check that .env file exists in api/ directory")
                print("   2. Verify credentials are set:")
                print("      HEDERA_TESTNET_OPERATOR_ID=0.0.xxxxxxx")
                print("      HEDERA_TESTNET_OPERATOR_KEY=302e...")
                print("   3. Restart the backend server")
    except Exception as e:
        print(f"❌ Error initializing HederaService: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

