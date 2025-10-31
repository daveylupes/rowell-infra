"""
Hedera Integration Validation Script
Tests real Hedera testnet integration for hackathon demo
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.hedera_service import HederaService
from api.core.config import settings
import structlog

logger = structlog.get_logger()


async def test_hedera_account_creation():
    """Test creating a real Hedera account on testnet"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Hedera Account Creation")
    print("="*60)
    
    service = HederaService(environment="testnet")
    
    try:
        print("\n📝 Creating account on Hedera testnet...")
        account = await service.create_account(
            account_type="user",
            metadata={"test": True, "validation": True}
        )
        
        print(f"\n✅ Account created successfully!")
        print(f"   Account ID: {account.get('account_id')}")
        print(f"   Network: {account.get('network')}")
        print(f"   Environment: {account.get('environment')}")
        
        if account.get('note'):
            print(f"   ⚠️  Note: {account.get('note')}")
        
        if account.get('private_key'):
            print(f"   🔑 Private Key: {account.get('private_key')[:20]}...")
        
        return account
    except Exception as e:
        print(f"\n❌ Failed to create account: {str(e)}")
        return None


async def test_hedera_account_info(account_id: str):
    """Test fetching account information from Hedera"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Hedera Account Information")
    print("="*60)
    
    service = HederaService(environment="testnet")
    
    try:
        print(f"\n📝 Fetching account info for {account_id}...")
        account_info = await service.get_account_info(account_id)
        
        if not account_info:
            print(f"\n⚠️  Account {account_id} not found (this is OK for testnet)")
            return None
        
        print(f"\n✅ Account info retrieved successfully!")
        print(f"   Account ID: {account_info.get('account_id')}")
        print(f"   Balance: {account_info.get('balance')} HBAR")
        print(f"   Balance (tinybars): {account_info.get('balance_tinybars')}")
        print(f"   Created: {account_info.get('created_timestamp')}")
        
        return account_info
    except Exception as e:
        print(f"\n❌ Failed to get account info: {str(e)}")
        return None


async def test_hedera_balance_query(account_id: str):
    """Test querying account balances"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Hedera Balance Query")
    print("="*60)
    
    service = HederaService(environment="testnet")
    
    try:
        print(f"\n📝 Querying balances for {account_id}...")
        balances = await service.get_account_balances(account_id)
        
        print(f"\n✅ Balances retrieved successfully!")
        print(f"   Found {len(balances)} asset(s):")
        
        for balance in balances:
            print(f"   - {balance.get('asset_code')}: {balance.get('balance')} "
                  f"(≈ ${balance.get('balance_usd', '0.00')} USD)")
        
        return balances
    except Exception as e:
        print(f"\n❌ Failed to query balances: {str(e)}")
        return None


async def test_hedera_payment_transaction():
    """Test creating a payment transaction (if SDK is available)"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Hedera Payment Transaction")
    print("="*60)
    
    service = HederaService(environment="testnet")
    
    # Check if SDK is available
    try:
        from hedera import Client, PrivateKey, AccountId, Hbar, TransferTransaction
        print("\n✅ Hedera SDK is available")
    except ImportError:
        print("\n⚠️  Hedera SDK not installed")
        print("   Install with: pip install hedera-sdk-py")
        print("   Also requires Java 17+ to be installed")
        return None
    
    # Check if operator is configured
    if not service.has_operator:
        print("\n⚠️  Hedera operator not configured")
        print("   Set environment variables:")
        print("   - HEDERA_TESTNET_OPERATOR_ID")
        print("   - HEDERA_TESTNET_OPERATOR_KEY")
        print("\n   Skipping transaction test...")
        return None
    
    print("\n📝 Transaction test would be executed here")
    print("   (Creating transactions requires funded accounts)")
    
    return None


async def check_hedera_mirror_node():
    """Test Hedera Mirror Node API connectivity"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Hedera Mirror Node API")
    print("="*60)
    
    import httpx
    
    try:
        print(f"\n📝 Testing connection to Hedera Mirror Node...")
        url = settings.HEDERA_TESTNET_URL
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{url}/api/v1/accounts/0.0.2")
            
            if response.status_code in [200, 404]:
                print(f"\n✅ Mirror Node API is accessible!")
                print(f"   URL: {url}")
                print(f"   Status: {response.status_code}")
                return True
            else:
                print(f"\n⚠️  Mirror Node returned status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"\n❌ Mirror Node API unreachable: {str(e)}")
        return False


async def validate_hedera_integration():
    """Main validation function"""
    print("\n" + "="*70)
    print("🚀 HEDERA INTEGRATION VALIDATION")
    print("="*70)
    print("\nThis script validates real Hedera testnet integration.")
    print("For hackathon demo, we need to ensure transactions work on testnet.\n")
    
    results = {
        "account_creation": False,
        "account_info": False,
        "balance_query": False,
        "mirror_node": False,
        "payment_transaction": False,
    }
    
    # Test 1: Account Creation
    account = await test_hedera_account_creation()
    if account:
        results["account_creation"] = True
        account_id = account.get("account_id")
        
        # Test 2: Account Info
        account_info = await test_hedera_account_info(account_id)
        if account_info:
            results["account_info"] = True
        
        # Test 3: Balance Query
        balances = await test_hedera_balance_query(account_id)
        if balances is not None:
            results["balance_query"] = True
    
    # Test 4: Payment Transaction
    await test_hedera_payment_transaction()
    # Note: Transaction test requires real operator credentials
    
    # Test 5: Mirror Node
    mirror_node_ok = await check_hedera_mirror_node()
    results["mirror_node"] = mirror_node_ok
    
    # Summary
    print("\n" + "="*70)
    print("📊 VALIDATION SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test.replace('_', ' ').title()}: {status}")
    
    print(f"\n   Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Hedera integration is ready for demo.")
    elif results["mirror_node"] and results["account_creation"]:
        print("\n✅ Core functionality works! Demo can proceed with read operations.")
        print("   For write operations, ensure Hedera SDK and operator are configured.")
    else:
        print("\n⚠️  Some tests failed. Review the output above.")
        print("   For hackathon demo:")
        print("   1. Ensure Hedera SDK is installed (if doing real transactions)")
        print("   2. Configure operator credentials via environment variables")
        print("   3. Mirror Node API should work without SDK")
    
    print("\n" + "="*70 + "\n")
    
    return results


if __name__ == "__main__":
    asyncio.run(validate_hedera_integration())

