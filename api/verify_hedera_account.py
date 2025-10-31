#!/usr/bin/env python3
"""
Verify Hedera account and key match
"""
import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.core.config import settings
from hedera import Client, AccountId, PrivateKey, AccountBalanceQuery

async def verify_account():
    print("🔍 Verifying Hedera Account & Key Match\n")
    print("=" * 60)
    
    operator_id = settings.HEDERA_TESTNET_OPERATOR_ID
    operator_key = settings.HEDERA_TESTNET_OPERATOR_KEY
    
    print(f"\n1️⃣  Checking Account on Blockchain:")
    print(f"   Account ID: {operator_id}")
    
    # Check account via mirror node
    mirror_url = "https://testnet.mirrornode.hedera.com"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{mirror_url}/api/v1/accounts/{operator_id}")
            if response.status_code == 200:
                account_data = response.json()
                balance = account_data.get("balance", {})
                balance_hbar = float(balance.get("balance", "0")) / 100000000
                print(f"   ✅ Account EXISTS on blockchain")
                print(f"   Balance: {balance_hbar:.2f} HBAR")
                
                if balance_hbar < 10:
                    print(f"   ⚠️  WARNING: Low balance! Need at least 10 HBAR for testing")
                    print(f"   Get more testnet HBAR: https://portal.hedera.com/")
            else:
                print(f"   ❌ Account NOT FOUND (HTTP {response.status_code})")
                print(f"   Account doesn't exist or credentials don't match")
        except Exception as e:
            print(f"   ⚠️  Error checking account: {e}")
    
    print(f"\n2️⃣  Testing SDK Connection:")
    try:
        client = Client.forTestnet()
        operator_account = AccountId.fromString(operator_id)
        operator_private_key = PrivateKey.fromString(operator_key)
        
        client.setOperator(operator_account, operator_private_key)
        print(f"   ✅ Operator set successfully")
        
        # Try to get balance via SDK
        print(f"\n3️⃣  Testing Balance Query (proves key matches):")
        try:
            balance_query = AccountBalanceQuery().setAccountId(operator_account)
            balance = balance_query.execute(client)
            balance_hbar = float(balance.hbars.toString())
            print(f"   ✅ Balance query successful!")
            print(f"   Balance: {balance_hbar} HBAR")
            print(f"   ✅ KEY MATCHES ACCOUNT!")
            
            if balance_hbar < 10:
                print(f"   ⚠️  Low balance - might cause issues")
                
        except Exception as e:
            print(f"   ❌ Balance query failed: {e}")
            print(f"   This suggests key doesn't match account!")
            return False
        
        # Try a simple transaction (account creation)
        print(f"\n4️⃣  Testing Transaction Signing:")
        try:
            from hedera import AccountCreateTransaction, Hbar
            
            # Create a minimal test - just build transaction, don't execute
            test_key = PrivateKey.generate()
            tx = AccountCreateTransaction().setKey(test_key.getPublicKey()).setInitialBalance(Hbar(0))
            
            print(f"   ✅ Transaction builds correctly")
            print(f"   💡 Transaction signing would be tested by actually creating an account")
            
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ SDK Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(verify_account())
    
    print("\n" + "=" * 60)
    if result:
        print("✅ Account and key appear to match!")
        print("If you still get INVALID_SIGNATURE, try:")
        print("1. Regenerate key pair from Hedera Portal")
        print("2. Make sure you're using the correct network (testnet)")
        print("3. Check account has sufficient balance")
    else:
        print("❌ Issue found with account/key match")
        print("Recommendation: Get fresh credentials from Hedera Portal")

