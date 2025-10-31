"""
Analytics service for Rowell Infra Python SDK
"""

from typing import List, Optional, Dict, Any
import httpx
from ..types import RemittanceFlow, StablecoinAdoption, MerchantActivity, NetworkMetrics


class AnalyticsService:
    """Service for analytics and reporting"""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
    
    async def get_remittance_flows(self, **kwargs) -> List[RemittanceFlow]:
        """Get remittance flow analytics"""
        response = await self.http_client.get('/api/v1/analytics/remittance', params=kwargs)
        response.raise_for_status()
        return [RemittanceFlow(**flow) for flow in response.json()]
    
    async def get_stablecoin_adoption(self, **kwargs) -> List[StablecoinAdoption]:
        """Get stablecoin adoption analytics"""
        response = await self.http_client.get('/api/v1/analytics/stablecoin', params=kwargs)
        response.raise_for_status()
        return [StablecoinAdoption(**adoption) for adoption in response.json()]
    
    async def get_merchant_activity(self, **kwargs) -> List[MerchantActivity]:
        """Get merchant activity analytics"""
        response = await self.http_client.get('/api/v1/analytics/merchants', params=kwargs)
        response.raise_for_status()
        return [MerchantActivity(**merchant) for merchant in response.json()]
    
    async def get_network_metrics(self, **kwargs) -> List[NetworkMetrics]:
        """Get network metrics"""
        response = await self.http_client.get('/api/v1/analytics/network', params=kwargs)
        response.raise_for_status()
        return [NetworkMetrics(**metric) for metric in response.json()]
    
    async def get_dashboard_data(self, **kwargs) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        response = await self.http_client.get('/api/v1/analytics/dashboard', params=kwargs)
        response.raise_for_status()
        return response.json()
