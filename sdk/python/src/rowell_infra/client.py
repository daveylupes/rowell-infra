"""
Rowell Infra Python SDK Client
Alchemy for Africa: Stellar + Hedera APIs & Analytics
"""

import asyncio
from typing import Optional, Dict, Any
import httpx
from .services import AccountService, TransferService, AnalyticsService, ComplianceService
from .types import RowellConfig


class RowellClient:
    """Main Rowell Infra client for Python SDK"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize Rowell Infra client
        
        Args:
            base_url: Base URL of the Rowell Infra API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # Create HTTP client
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Rowell-Infra-SDK-Python/1.0.0'
        }
        
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        self.http_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout
        )
        
        # Initialize services
        self.accounts = AccountService(self.http_client)
        self.transfers = TransferService(self.http_client)
        self.analytics = AnalyticsService(self.http_client)
        self.compliance = ComplianceService(self.http_client)
    
    async def get_health(self) -> Dict[str, Any]:
        """Get API health status"""
        response = await self.http_client.get('/health')
        response.raise_for_status()
        return response.json()
    
    async def get_info(self) -> Dict[str, Any]:
        """Get API information"""
        response = await self.http_client.get('/')
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client"""
        await self.http_client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
