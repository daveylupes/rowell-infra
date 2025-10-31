#!/usr/bin/env python3
"""
Test script to verify account creation is working and creating REAL accounts
"""
import asyncio
import sys
import os
import httpx
import json

# Add api directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.services.hedera_service import HederaService
from api.core.config import settings

async def test_account_creation():
    print("🧪 Testing Account Creation\n")
    print("=" * 60)
    
    # Check credentials
    print("\n1️⃣  Checking Hedera Configuration...")
    has_id = bool(settings.HEDERA_TESTNET_OPERATOR_ID)
    has_key = bool(settings.HEDERA_TESTNET_OPERATOR_KEY)
    
    print(f"   Operator ID set: {'✅' if has_id else '❌'}")
    if has_id:
        id_val = settings.HEDERA_TESTNET_OPERATOR_ID
        print(f"   ID: {id_val[:10]}...{id_val[-4:] if len(id_val) > 14 else id_val}")
    
    print(f"   Operator Key set: {'✅' if has_key else '❌'}")
    if has_key:
        key_val = settings.HEDERA_TESTNET_OPERATOR_KEY
        print(f"   Key: {key_val[:20]}...{key_val[-10:] if len(key_val) > 30 else key_val}")
    
    if not has_id or not has_key:
        print("\n❌ Credentials not set! Cannot create real accounts.")
        return False
    
    # Test HederaService
    print("\n2️⃣  Testing HederaService...")
    try:
        service = HederaService(environment="testnet")
        if not service.has_operator:
            print("   ❌ HederaService NOT configured with operator")
            print("   ⚠️  This means accounts will be created in MOCK mode!")
            return False
        print("   ✅ HederaService configured with operator")
        print("   ✅ Real account creation enabled")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test actual account creation
    print("\n3️⃣  Testing Account Creation...")
    try:
        result = await service.create_account(
            account_type="user",
            metadata={"test": "script"}
        )
        
        account_id = result.get("account_id")
        # Convert AccountId object to string if needed
        if hasattr(account_id, '__str__') and not isinstance(account_id, str):
            account_id = str(account_id)
        
        private_key = result.get("private_key", "")
        
        print(f"   Account ID: {account_id}")
        
        # Check if it's a mock account
        is_mock = (
            "note" in result and "mock" in result.get("note", "").lower()
        ) or private_key.startswith("mock_hedera_private_")
        
        if is_mock:
            print("   ❌ MOCK ACCOUNT CREATED!")
            print(f"   Reason: {result.get('note', 'Unknown')}")
            print("   ⚠️  This account will NOT exist on blockchain")
            return False
        else:
            print("   ✅ REAL ACCOUNT CREATED!")
            print(f"   Private key format: {private_key[:30]}...")
            print("   ✅ This account should exist on blockchain")
        
        # Verify on HashScan
        print(f"\n4️⃣  Verifying on HashScan...")
        print(f"   URL: https://hashscan.io/testnet/account/{account_id}")
        
        mirror_url = "https://testnet.mirrornode.hedera.com"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{mirror_url}/api/v1/accounts/{account_id}")
            
            if response.status_code == 200:
                account_data = response.json()
                balance = account_data.get("balance", {})
                balance_hbar = balance.get("balance", "0")
                print(f"   ✅ Account EXISTS on blockchain!")
                print(f"   Balance: {balance_hbar} tinybars (~{float(balance_hbar)/100000000:.2f} HBAR)")
                return True
            elif response.status_code == 404:
                print(f"   ❌ Account NOT FOUND on blockchain")
                print("   ⚠️  This means it's a mock account or wasn't created")
                return False
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error creating account: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_endpoint(api_key: str):
    """Test the actual API endpoint"""
    print("\n" + "=" * 60)
    print("5️⃣  Testing API Endpoint...")
    print(f"   API Key: {api_key[:20]}...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/api/v1/accounts/create",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "network": "hedera",
                    "environment": "testnet",
                    "account_type": "user",
                    "country_code": "NG"
                }
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                account_id = data.get("account_id")
                print(f"   Account ID: {account_id}")
                
                # Check if mock
                response_text = response.text
                if "mock" in response_text.lower() or "note" in data:
                    print("   ❌ MOCK ACCOUNT RETURNED!")
                    return False
                else:
                    print("   ✅ Account created via API")
                    
                    # Verify on blockchain
                    print(f"\n   Verifying on HashScan: https://hashscan.io/testnet/account/{account_id}")
                    mirror_response = await httpx.AsyncClient().get(
                        f"https://testnet.mirrornode.hedera.com/api/v1/accounts/{account_id}"
                    )
                    
                    if mirror_response.status_code == 200:
                        print("   ✅ Account EXISTS on blockchain!")
                        return True
                    else:
                        print(f"   ❌ Account NOT on blockchain (HTTP {mirror_response.status_code})")
                        return False
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def main():
    print("🚀 Account Creation Test Script\n")
    
    # Test 1: Direct service test
    result1 = await test_account_creation()
    
    # Test 2: API endpoint test (if API key provided)
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        result2 = await test_api_endpoint(api_key)
    else:
        print("\n💡 To test API endpoint, run:")
        print("   python test_account_creation.py ri_YOUR_API_KEY")
        result2 = None
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Direct Service Test: {'✅ PASS' if result1 else '❌ FAIL'}")
    if result2 is not None:
        print(f"API Endpoint Test: {'✅ PASS' if result2 else '❌ FAIL'}")
    
    if not result1:
        print("\n⚠️  ISSUE FOUND:")
        print("   Accounts are being created in MOCK mode")
        print("   Check:")
        print("   1. Hedera credentials in api/.env")
        print("   2. Backend logs for errors")
        print("   3. Operator account has sufficient HBAR balance")

if __name__ == "__main__":
    asyncio.run(main())

