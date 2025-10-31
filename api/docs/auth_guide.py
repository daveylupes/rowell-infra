"""
Authentication guide for Rowell Infra API
"""

from typing import Dict, List, Any


class AuthenticationGuide:
    """Comprehensive authentication guide and examples"""
    
    @staticmethod
    def get_authentication_overview() -> Dict[str, Any]:
        """Get authentication overview and requirements"""
        return {
            "overview": {
                "title": "API Authentication",
                "description": "The Rowell Infra API uses API key-based authentication for secure access to endpoints.",
                "authentication_method": "API Key",
                "header_name": "X-API-Key",
                "security_level": "High - All requests are encrypted via HTTPS"
            },
            "requirements": [
                "Valid API key from your Rowell Infra dashboard",
                "HTTPS connection (HTTP not supported in production)",
                "Proper header format: X-API-Key: your_key_here"
            ],
            "supported_environments": [
                "Production (api.rowellinfra.com)",
                "Staging (api-staging.rowellinfra.com)",
                "Development (localhost:8000)"
            ]
        }
    
    @staticmethod
    def get_api_key_guide() -> Dict[str, Any]:
        """Get API key management guide"""
        return {
            "getting_api_key": {
                "title": "Getting Your API Key",
                "steps": [
                    "1. Sign up for a Rowell Infra account at dashboard.rowellinfra.com",
                    "2. Complete the account verification process",
                    "3. Navigate to the API Keys section in your dashboard",
                    "4. Click 'Generate New API Key'",
                    "5. Copy and securely store your API key",
                    "6. Note the key's permissions and expiration date"
                ],
                "important_notes": [
                    "API keys are only shown once during creation",
                    "Store your API key securely - it cannot be recovered",
                    "Different keys can have different permission levels",
                    "Keys can be revoked or regenerated at any time"
                ]
            },
            "api_key_format": {
                "title": "API Key Format",
                "description": "API keys follow a specific format for security and identification",
                "format": "ri_[environment]_[random_string]_[checksum]",
                "examples": [
                    # NOTE: These are example/dummy keys for documentation only
                    # Never use these in production - they are invalid placeholder keys
                    "ri_prod_abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
                    "ri_test_xyz789abc123def456ghi789jkl012mno345pqr678stu901vw",
                    "ri_dev_def456ghi789jkl012mno345pqr678stu901vwx234yz567abc"
                ],
                "components": {
                    "ri": "Rowell Infra identifier",
                    "prod/test/dev": "Environment indicator",
                    "random_string": "Cryptographically secure random string",
                    "checksum": "Verification checksum"
                }
            },
            "permissions": {
                "title": "API Key Permissions",
                "description": "API keys can have different permission levels based on your plan",
                "permission_levels": {
                    "read": "Read-only access to accounts, transfers, and analytics",
                    "write": "Create and update accounts and transfers",
                    "admin": "Full administrative access including compliance operations"
                },
                "scopes": {
                    "accounts:read": "View account information and balances",
                    "accounts:write": "Create and update accounts",
                    "transfers:read": "View transfer information and status",
                    "transfers:write": "Create and manage transfers",
                    "analytics:read": "Access analytics and reporting data",
                    "compliance:read": "View compliance and KYC information",
                    "compliance:write": "Manage compliance flags and KYC verifications"
                }
            }
        }
    
    @staticmethod
    def get_authentication_examples() -> Dict[str, Any]:
        """Get authentication examples for different languages and tools"""
        return {
            "curl": {
                "title": "cURL Examples",
                "basic_request": """
curl -X GET "https://api.rowellinfra.com/api/v1/accounts" \\
  -H "X-API-Key: your_api_key_here"
""",
                "post_request": """
curl -X POST "https://api.rowellinfra.com/api/v1/accounts" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: your_api_key_here" \\
  -d '{"network": "stellar", "environment": "testnet"}'
"""
            },
            "javascript": {
                "title": "JavaScript Examples",
                "fetch_api": """
// Using fetch API
const response = await fetch('https://api.rowellinfra.com/api/v1/accounts', {
  method: 'GET',
  headers: {
    'X-API-Key': 'your_api_key_here',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
""",
                "axios": """
// Using axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.rowellinfra.com/api/v1',
  headers: {
    'X-API-Key': 'your_api_key_here'
  }
});

const response = await api.get('/accounts');
""",
                "nodejs": """
// Using node-fetch in Node.js
const fetch = require('node-fetch');

const response = await fetch('https://api.rowellinfra.com/api/v1/accounts', {
  headers: {
    'X-API-Key': 'your_api_key_here'
  }
});

const data = await response.json();
"""
            },
            "python": {
                "title": "Python Examples",
                "requests": """
import requests

headers = {
    'X-API-Key': 'your_api_key_here',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.rowellinfra.com/api/v1/accounts',
    headers=headers
)

data = response.json()
""",
                "httpx": """
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        'https://api.rowellinfra.com/api/v1/accounts',
        headers={'X-API-Key': 'your_api_key_here'}
    )
    
    data = response.json()
""",
                "class_based": """
class RowellInfraClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.rowellinfra.com/api/v1'
    
    def _get_headers(self):
        return {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def get_accounts(self):
        response = requests.get(
            f'{self.base_url}/accounts',
            headers=self._get_headers()
        )
        return response.json()

# Usage
client = RowellInfraClient('your_api_key_here')
accounts = client.get_accounts()
"""
            }
        }
    
    @staticmethod
    def get_security_best_practices() -> Dict[str, Any]:
        """Get security best practices for API key management"""
        return {
            "api_key_security": [
                "Never expose API keys in client-side code",
                "Store API keys in environment variables",
                "Use different keys for different environments",
                "Rotate API keys regularly",
                "Monitor API key usage for suspicious activity",
                "Revoke unused or compromised keys immediately"
            ],
            "secure_storage": {
                "environment_variables": """
# Recommended: Store in environment variables
export ROWELL_API_KEY="your_api_key_here"

# In your code
import os
api_key = os.getenv('ROWELL_API_KEY')
""",
                "config_files": """
# .env file (add to .gitignore)
ROWELL_API_KEY=your_api_key_here
ROWELL_ENVIRONMENT=testnet

# Load with python-dotenv
from dotenv import load_dotenv
load_dotenv()
""",
                "secure_vaults": [
                    "Use secret management services (AWS Secrets Manager, Azure Key Vault)",
                    "Implement key rotation policies",
                    "Use least privilege access principles",
                    "Monitor and audit key usage"
                ]
            },
            "common_mistakes": [
                "Hardcoding API keys in source code",
                "Committing API keys to version control",
                "Using production keys in development",
                "Sharing API keys in unsecured channels",
                "Not monitoring API key usage",
                "Using overly permissive key scopes"
            ],
            "troubleshooting": {
                "invalid_key": {
                    "symptoms": "401 Unauthorized errors",
                    "causes": [
                        "Incorrect API key format",
                        "Expired or revoked key",
                        "Wrong environment (prod vs test)"
                    ],
                    "solutions": [
                        "Verify key format and value",
                        "Check key expiration date",
                        "Ensure using correct environment key"
                    ]
                },
                "insufficient_permissions": {
                    "symptoms": "403 Forbidden errors",
                    "causes": [
                        "Key lacks required permissions",
                        "Account plan limitations",
                        "Resource-specific restrictions"
                    ],
                    "solutions": [
                        "Check key permissions in dashboard",
                        "Upgrade account plan if needed",
                        "Contact support for permission changes"
                    ]
                }
            }
        }
    
    @staticmethod
    def get_authentication_flow() -> Dict[str, Any]:
        """Get authentication flow diagram and explanation"""
        return {
            "flow_diagram": """
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │   Rowell    │    │  Database   │
│ Application │    │    API      │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 1. Request +     │                  │
       │    API Key       │                  │
       ├─────────────────►│                  │
       │                  │                  │
       │                  │ 2. Validate Key  │
       │                  ├─────────────────►│
       │                  │                  │
       │                  │ 3. Key Valid     │
       │                  │◄─────────────────┤
       │                  │                  │
       │                  │ 4. Check         │
       │                  │    Permissions   │
       │                  ├─────────────────►│
       │                  │                  │
       │                  │ 5. Permissions   │
       │                  │    OK            │
       │                  │◄─────────────────┤
       │                  │                  │
       │ 6. Response      │                  │
       │◄─────────────────┤                  │
""",
            "flow_steps": [
                {
                    "step": 1,
                    "title": "Client Request",
                    "description": "Client sends request with API key in X-API-Key header"
                },
                {
                    "step": 2,
                    "title": "Key Validation",
                    "description": "API validates the key format, existence, and expiration"
                },
                {
                    "step": 3,
                    "title": "Permission Check",
                    "description": "API checks if key has required permissions for the operation"
                },
                {
                    "step": 4,
                    "title": "Request Processing",
                    "description": "If authenticated and authorized, process the request"
                },
                {
                    "step": 5,
                    "title": "Response",
                    "description": "Return response with data or error message"
                }
            ],
            "error_handling": {
                "401_unauthorized": "Invalid or missing API key",
                "403_forbidden": "Valid key but insufficient permissions",
                "429_rate_limit": "Too many requests with this key"
            }
        }
