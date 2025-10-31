"""
Account service for Rowell Infra Python SDK
"""

from typing import List, Optional, Dict, Any
import httpx
from ..types import Account, AccountBalance, CreateAccountRequest


class AccountService:
    """Service for managing accounts"""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
    
    async def create(self, **kwargs) -> Account:
        """Create a new account"""
        request = CreateAccountRequest(**kwargs)
        response = await self.http_client.post('/api/v1/accounts/create', json=request.dict())
        response.raise_for_status()
        return Account(**response.json())
    
    async def get(self, account_id: str) -> Account:
        """Get account by ID"""
        response = await self.http_client.get(f'/api/v1/accounts/{account_id}')
        response.raise_for_status()
        return Account(**response.json())
    
    async def get_balances(self, account_id: str) -> List[AccountBalance]:
        """Get account balances"""
        response = await self.http_client.get(f'/api/v1/accounts/{account_id}/balances')
        response.raise_for_status()
        return [AccountBalance(**balance) for balance in response.json()]
    
    async def list(self, **kwargs) -> List[Account]:
        """List accounts with optional filtering"""
        response = await self.http_client.get('/api/v1/accounts/', params=kwargs)
        response.raise_for_status()
        return [Account(**account) for account in response.json()]
