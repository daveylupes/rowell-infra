"""
Developer and user management schemas
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# Request schemas
class DeveloperRegistrationRequest(BaseModel):
    """Developer registration request"""
    email: EmailStr = Field(..., description="Developer email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    role: Optional[str] = Field(None, max_length=100, description="Job role")
    country_code: Optional[str] = Field(None, max_length=2, description="ISO country code")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    
    @validator('country_code')
    def validate_country_code(cls, v):
        if v and len(v) != 2:
            raise ValueError('Country code must be 2 characters (ISO format)')
        return v.upper() if v else v


class ProjectCreateRequest(BaseModel):
    """Project creation request"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    primary_network: str = Field("stellar", description="Primary blockchain network")
    environment: str = Field("testnet", description="Environment (testnet/mainnet)")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")
    
    @validator('primary_network')
    def validate_network(cls, v):
        if v not in ['stellar', 'hedera']:
            raise ValueError('Primary network must be stellar or hedera')
        return v
    
    @validator('environment')
    def validate_environment(cls, v):
        if v not in ['testnet', 'mainnet']:
            raise ValueError('Environment must be testnet or mainnet')
        return v


class APIKeyCreateRequest(BaseModel):
    """API key creation request"""
    key_name: str = Field(..., min_length=1, max_length=255, description="API key name")
    permissions: List[str] = Field(default_factory=list, description="API key permissions")
    rate_limit: int = Field(1000, ge=1, le=10000, description="Rate limit per hour")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")


class LoginRequest(BaseModel):
    """Developer login request"""
    email: EmailStr = Field(..., description="Developer email")
    # Note: In production, you'd want to add password field here


# Response schemas
class DeveloperResponse(BaseModel):
    """Developer response"""
    id: str
    email: str
    first_name: str
    last_name: str
    company: Optional[str] = None
    role: Optional[str] = None
    country_code: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    email_verified_at: Optional[datetime] = None
    created_at: str
    updated_at: Optional[str] = None
    last_login: Optional[str] = None
    
    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    """Project response"""
    id: str
    name: str
    description: Optional[str] = None
    primary_network: str
    environment: str
    webhook_url: Optional[str] = None
    is_active: bool
    is_public: bool
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class APIKeyResponse(BaseModel):
    """API key response (without the actual key)"""
    id: str
    key_name: str
    key_prefix: str
    permissions: List[str]
    rate_limit: int
    is_active: bool
    last_used: Optional[str] = None
    usage_count: int
    created_at: str
    expires_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class APIKeyWithSecretResponse(BaseModel):
    """API key response with the actual key (only shown once)"""
    id: str
    key_name: str
    api_key: str  # The actual API key
    key_prefix: str
    permissions: List[str]
    rate_limit: int
    is_active: bool
    created_at: str
    expires_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class DeveloperDashboardResponse(BaseModel):
    """Developer dashboard data"""
    developer: DeveloperResponse
    projects: List[ProjectResponse]
    api_keys: List[APIKeyResponse]
    stats: Dict[str, Any]


class QuickStartResponse(BaseModel):
    """Quick start response with developer, project, API key and example code"""
    developer: DeveloperResponse
    project: ProjectResponse
    api_key: APIKeyWithSecretResponse
    example_code: Dict[str, str]  # Language -> code example


# Update existing Account model to include project relationship
class AccountWithProjectResponse(BaseModel):
    """Account response with project information"""
    id: str
    account_id: str
    network: str
    environment: str
    account_type: str
    country_code: str
    region: Optional[str]
    is_active: bool
    is_verified: bool
    is_compliant: bool
    kyc_status: str
    created_at: datetime
    updated_at: datetime
    last_activity: Optional[datetime]
    metadata: Optional[Dict[str, Any]]
    project_id: Optional[UUID]
    project_name: Optional[str]
    
    class Config:
        from_attributes = True
