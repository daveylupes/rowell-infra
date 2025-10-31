#!/usr/bin/env python3
"""
Diagnostic script to check Hedera private key format
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.core.config import settings

def check_key_format():
    print("🔍 Hedera Key Diagnostic\n")
    print("=" * 60)
    
    operator_id = settings.HEDERA_TESTNET_OPERATOR_ID
    operator_key = settings.HEDERA_TESTNET_OPERATOR_KEY
    
    print(f"\n1️⃣  Operator Account ID:")
    print(f"   {operator_id}")
    print(f"   Format check: {'✅ Valid' if operator_id and operator_id.startswith('0.0.') else '❌ Invalid'}")
    
    print(f"\n2️⃣  Private Key Analysis:")
    if not operator_key:
        print("   ❌ Key is empty!")
        return
    
    print(f"   Length: {len(operator_key)} characters")
    print(f"   Starts with: {operator_key[:10]}...")
    print(f"   Ends with: ...{operator_key[-10:]}")
    
    # Check format
    if operator_key.startswith('302e'):
        print("   ✅ Format: DER encoded (correct)")
    elif operator_key.startswith('-----BEGIN'):
        print("   ❌ Format: PEM (wrong - needs DER)")
        print("   ⚠️  Hedera SDK needs DER format, not PEM")
    elif len(operator_key) == 64:
        print("   ⚠️  Format: Raw hex (might work, but DER is preferred)")
    else:
        print("   ⚠️  Format: Unknown")
    
    # Check for common issues
    print(f"\n3️⃣  Common Issues Check:")
    issues = []
    
    if ' ' in operator_key:
        issues.append("   ❌ Contains spaces")
    if '\n' in operator_key:
        issues.append("   ❌ Contains newlines")
    if operator_key.count('0') + operator_key.count('1') + operator_key.count('2') + operator_key.count('3') + operator_key.count('4') + operator_key.count('5') + operator_key.count('6') + operator_key.count('7') + operator_key.count('8') + operator_key.count('9') + operator_key.count('a') + operator_key.count('b') + operator_key.count('c') + operator_key.count('d') + operator_key.count('e') + operator_key.count('f') < len(operator_key) * 0.9:
        issues.append("   ⚠️  Contains non-hex characters")
    
    if not issues:
        print("   ✅ No obvious formatting issues")
    else:
        for issue in issues:
            print(issue)
    
    # Try to parse with SDK
    print(f"\n4️⃣  SDK Parsing Test:")
    try:
        from hedera import PrivateKey, AccountId
        
        # Try parsing account ID
        try:
            account = AccountId.fromString(operator_id)
            print(f"   ✅ Account ID parses correctly: {account}")
        except Exception as e:
            print(f"   ❌ Account ID parse error: {e}")
        
        # Try parsing private key
        try:
            key = PrivateKey.fromString(operator_key)
            print(f"   ✅ Private key parses correctly")
            print(f"   Public key: {key.getPublicKey().toString()[:50]}...")
        except Exception as e:
            print(f"   ❌ Private key parse error: {e}")
            print(f"   This is likely the issue!")
            
    except ImportError:
        print("   ⚠️  Hedera SDK not available")
    
    print("\n" + "=" * 60)
    print("💡 Troubleshooting Tips:")
    print("=" * 60)
    print("1. Make sure private key is DER format (starts with 302e...)")
    print("2. Key should be exported from Hedera Portal as 'DER' or 'Raw' format")
    print("3. No quotes, spaces, or newlines in .env file")
    print("4. Verify key matches the account ID in Hedera Portal")
    print("5. If key was exported as PEM, convert to DER:")
    print("   openssl ec -in key.pem -outform DER -out key.der")
    print("   then convert DER to hex string")

if __name__ == "__main__":
    check_key_format()

