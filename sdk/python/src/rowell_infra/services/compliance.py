"""
Compliance service for Rowell Infra Python SDK
"""

from typing import List, Optional, Dict, Any
import httpx
from ..types import KYCVerification, ComplianceFlag, ComplianceReport, CreateKYCVerificationRequest, CreateComplianceFlagRequest


class ComplianceService:
    """Service for compliance and KYC operations"""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
    
    async def verify_id(self, **kwargs) -> KYCVerification:
        """Initiate KYC verification"""
        request = CreateKYCVerificationRequest(**kwargs)
        response = await self.http_client.post('/api/v1/compliance/verify-id', json=request.dict())
        response.raise_for_status()
        return KYCVerification(**response.json())
    
    async def get_kyc_verification(self, verification_id: str) -> KYCVerification:
        """Get KYC verification status"""
        response = await self.http_client.get(f'/api/v1/compliance/verify-id/{verification_id}')
        response.raise_for_status()
        return KYCVerification(**response.json())
    
    async def flag_transaction(self, **kwargs) -> ComplianceFlag:
        """Flag a transaction or account for compliance review"""
        request = CreateComplianceFlagRequest(**kwargs)
        response = await self.http_client.post('/api/v1/compliance/flag-transaction', json=request.dict())
        response.raise_for_status()
        return ComplianceFlag(**response.json())
    
    async def list_compliance_flags(self, **kwargs) -> List[ComplianceFlag]:
        """List compliance flags with optional filtering"""
        response = await self.http_client.get('/api/v1/compliance/flags', params=kwargs)
        response.raise_for_status()
        return [ComplianceFlag(**flag) for flag in response.json()]
    
    async def get_compliance_reports(self, **kwargs) -> List[ComplianceReport]:
        """Get compliance reports"""
        response = await self.http_client.get('/api/v1/compliance/reports', params=kwargs)
        response.raise_for_status()
        return [ComplianceReport(**report) for report in response.json()]
