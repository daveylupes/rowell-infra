"""
Transfer service for Rowell Infra Python SDK
"""

from typing import List, Optional, Dict, Any
import httpx
from ..types import Transfer, TransferRequest, TransferStatus


class TransferService:
    """Service for managing transfers"""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
    
    async def create(self, **kwargs) -> Transfer:
        """Create a new transfer"""
        request = TransferRequest(**kwargs)
        response = await self.http_client.post('/api/v1/transfers/create', json=request.dict())
        response.raise_for_status()
        return Transfer(**response.json())
    
    async def get(self, transaction_hash: str) -> Transfer:
        """Get transfer by transaction hash"""
        response = await self.http_client.get(f'/api/v1/transfers/{transaction_hash}')
        response.raise_for_status()
        return Transfer(**response.json())
    
    async def get_status(self, transaction_hash: str) -> TransferStatus:
        """Get transfer status"""
        response = await self.http_client.get(f'/api/v1/transfers/{transaction_hash}/status')
        response.raise_for_status()
        return TransferStatus(**response.json())
    
    async def list(self, **kwargs) -> List[Transfer]:
        """List transfers with optional filtering"""
        response = await self.http_client.get('/api/v1/transfers/', params=kwargs)
        response.raise_for_status()
        return [Transfer(**transfer) for transfer in response.json()]
