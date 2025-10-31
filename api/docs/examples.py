"""
Code examples for Rowell Infra API
"""

from typing import Dict, List, Any


class CodeExamples:
    """Code examples for different programming languages"""
    
    @staticmethod
    def get_javascript_examples() -> Dict[str, Any]:
        """Get JavaScript/TypeScript code examples"""
        return {
            "account_creation": {
                "title": "Create Account (JavaScript)",
                "description": "Create a new blockchain account",
                "code": """
// Using fetch API
const response = await fetch('https://api.rowellinfra.com/api/v1/accounts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your_api_key_here'
  },
  body: JSON.stringify({
    network: 'stellar',
    environment: 'testnet',
    account_type: 'individual',
    country_code: 'NG'
  })
});

const account = await response.json();
console.log('Created account:', account);

// Using axios
import axios from 'axios';

const createAccount = async () => {
  try {
    const response = await axios.post(
      'https://api.rowellinfra.com/api/v1/accounts',
      {
        network: 'stellar',
        environment: 'testnet', 
        account_type: 'individual',
        country_code: 'NG'
      },
      {
        headers: {
          'X-API-Key': 'your_api_key_here'
        }
      }
    );
    
    console.log('Account created:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error creating account:', error.response.data);
  }
};
"""
            },
            "transfer_creation": {
                "title": "Create Transfer (JavaScript)",
                "description": "Send a payment transfer",
                "code": """
const createTransfer = async () => {
  const transferData = {
    from_account: 'account_id_here',
    to_account: 'recipient_account_id',
    asset_code: 'USDC',
    amount: '100.00',
    network: 'stellar',
    environment: 'testnet',
    memo: 'Payment for services'
  };

  try {
    const response = await fetch('https://api.rowellinfra.com/api/v1/transfers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your_api_key_here'
      },
      body: JSON.stringify(transferData)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const transfer = await response.json();
    console.log('Transfer created:', transfer);
    return transfer;
  } catch (error) {
    console.error('Transfer failed:', error);
  }
};
"""
            },
            "account_listing": {
                "title": "List Accounts (JavaScript)",
                "description": "Retrieve paginated list of accounts",
                "code": """
const listAccounts = async (page = 0, limit = 10) => {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: (page * limit).toString(),
    network: 'stellar',
    environment: 'testnet'
  });

  try {
    const response = await fetch(
      `https://api.rowellinfra.com/api/v1/accounts?${params}`,
      {
        headers: {
          'X-API-Key': 'your_api_key_here'
        }
      }
    );

    const data = await response.json();
    console.log('Accounts:', data.accounts);
    console.log('Pagination:', data.pagination);
    return data;
  } catch (error) {
    console.error('Error listing accounts:', error);
  }
};
"""
            }
        }
    
    @staticmethod
    def get_python_examples() -> Dict[str, Any]:
        """Get Python code examples"""
        return {
            "account_creation": {
                "title": "Create Account (Python)",
                "description": "Create a new blockchain account",
                "code": """
import requests
import json

def create_account():
    url = "https://api.rowellinfra.com/api/v1/accounts"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "your_api_key_here"
    }
    data = {
        "network": "stellar",
        "environment": "testnet",
        "account_type": "individual", 
        "country_code": "NG"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        account = response.json()
        print(f"Created account: {account}")
        return account
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating account: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

# Using async/await with httpx
import httpx
import asyncio

async def create_account_async():
    url = "https://api.rowellinfra.com/api/v1/accounts"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "your_api_key_here"
    }
    data = {
        "network": "stellar",
        "environment": "testnet",
        "account_type": "individual",
        "country_code": "NG"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            account = response.json()
            print(f"Created account: {account}")
            return account
            
        except httpx.RequestError as e:
            print(f"Error creating account: {e}")

# Run async function
# asyncio.run(create_account_async())
"""
            },
            "transfer_creation": {
                "title": "Create Transfer (Python)",
                "description": "Send a payment transfer",
                "code": """
def create_transfer(from_account, to_account, amount, asset_code="USDC"):
    url = "https://api.rowellinfra.com/api/v1/transfers"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "your_api_key_here"
    }
    data = {
        "from_account": from_account,
        "to_account": to_account,
        "asset_code": asset_code,
        "amount": str(amount),
        "network": "stellar",
        "environment": "testnet",
        "memo": "Payment for services"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        transfer = response.json()
        print(f"Transfer created: {transfer}")
        return transfer
        
    except requests.exceptions.RequestException as e:
        print(f"Transfer failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

# Usage
# transfer = create_transfer("from_account_id", "to_account_id", "100.00")
"""
            },
            "kyc_verification": {
                "title": "KYC Verification (Python)",
                "description": "Initiate KYC verification",
                "code": """
def initiate_kyc_verification(account_id, verification_data):
    url = "https://api.rowellinfra.com/api/v1/compliance/verify-id"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "your_api_key_here"
    }
    
    data = {
        "account_id": account_id,
        "network": "stellar",
        "verification_type": "individual",
        "first_name": verification_data.get("first_name"),
        "last_name": verification_data.get("last_name"),
        "date_of_birth": verification_data.get("date_of_birth"),
        "nationality": verification_data.get("nationality"),
        "document_type": "bvn",
        "bvn": verification_data.get("bvn")
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        verification = response.json()
        print(f"KYC verification initiated: {verification}")
        return verification
        
    except requests.exceptions.RequestException as e:
        print(f"KYC verification failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

# Usage
# verification_data = {
#     "first_name": "John",
#     "last_name": "Doe", 
#     "date_of_birth": "1990-01-01",
#     "nationality": "NG",
#     "bvn": "12345678901"
# }
# verification = initiate_kyc_verification("account_id", verification_data)
"""
            }
        }
    
    @staticmethod
    def get_curl_examples() -> Dict[str, Any]:
        """Get cURL code examples"""
        return {
            "account_creation": {
                "title": "Create Account (cURL)",
                "description": "Create a new blockchain account using cURL",
                "code": """
curl -X POST "https://api.rowellinfra.com/api/v1/accounts" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: your_api_key_here" \\
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "individual",
    "country_code": "NG"
  }'
"""
            },
            "transfer_creation": {
                "title": "Create Transfer (cURL)",
                "description": "Send a payment transfer using cURL",
                "code": """
curl -X POST "https://api.rowellinfra.com/api/v1/transfers" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: your_api_key_here" \\
  -d '{
    "from_account": "account_id_here",
    "to_account": "recipient_account_id",
    "asset_code": "USDC",
    "amount": "100.00",
    "network": "stellar",
    "environment": "testnet",
    "memo": "Payment for services"
  }'
"""
            },
            "account_listing": {
                "title": "List Accounts (cURL)",
                "description": "Retrieve list of accounts using cURL",
                "code": """
curl -X GET "https://api.rowellinfra.com/api/v1/accounts?limit=10&offset=0&network=stellar" \\
  -H "X-API-Key: your_api_key_here"
"""
            }
        }
    
    @staticmethod
    def get_all_examples() -> Dict[str, Any]:
        """Get all code examples organized by language"""
        return {
            "javascript": CodeExamples.get_javascript_examples(),
            "python": CodeExamples.get_python_examples(),
            "curl": CodeExamples.get_curl_examples()
        }
