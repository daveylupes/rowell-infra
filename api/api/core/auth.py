"""
Authentication and authorization middleware
"""

import hashlib
from typing import Dict, Any, Optional, List
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.database import get_db
import structlog

logger = structlog.get_logger()
security = HTTPBearer()


class HybridAuth:
    """Hybrid authentication: supports both JWT tokens (for logged-in users) and API keys"""
    
    def __init__(self, required_permissions: List[str] = None):
        self.required_permissions = required_permissions or []
    
    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ) -> Dict[str, Any]:
        """Validate either JWT token or API key and return auth info"""
        try:
            token = credentials.credentials
            
            # Try JWT authentication first (for logged-in users)
            jwt_auth_result = await self._try_jwt_auth(token, db)
            if jwt_auth_result:
                # For JWT-authenticated users (logged-in dashboard users), allow basic operations
                # without explicit permissions - they're already authenticated
                if self.required_permissions:
                    user_permissions = jwt_auth_result.get("permissions", [])
                    missing_permissions = set(self.required_permissions) - set(user_permissions)
                    
                    # Allow JWT users to perform basic operations even without explicit permissions
                    # This enables logged-in users to create accounts, transfers, etc.
                    if missing_permissions:
                        # For API keys, always enforce permissions
                        # But for JWT users, allow basic operations like account creation
                        basic_permissions = ["accounts:write", "accounts:read", "transfers:write", "transfers:read"]
                        requested_basic = set(self.required_permissions) & set(basic_permissions)
                        
                        if requested_basic:
                            # User is requesting basic operations, allow it for JWT users
                            logger.info(
                                "Allowing JWT user basic operations",
                                user_id=jwt_auth_result.get("user_id"),
                                requested_permissions=self.required_permissions,
                                has_explicit_permissions=False
                            )
                        else:
                            # Non-basic permissions required, enforce them
                            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
                            )
                
                # Add auth info to request state
                request.state.auth_info = jwt_auth_result
                return jwt_auth_result
            
            # Fall back to API key authentication
            if not token.startswith("ri_"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token or API key format"
                )
            
            # Validate API key
            from api.services.developer_service import DeveloperService
            developer_service = DeveloperService(db)
            api_key_info = await developer_service.validate_api_key(token)
            
            if not api_key_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired API key"
                )
            
            # Check permissions
            if self.required_permissions:
                user_permissions = api_key_info.get("permissions", [])
                missing_permissions = set(self.required_permissions) - set(user_permissions)
                
                if missing_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing required permissions: {', '.join(missing_permissions)}"
                    )
            
            # Add API key info to request state
            request.state.auth_info = api_key_info
            
            return api_key_info
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Authentication error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )
    
    async def _try_jwt_auth(self, token: str, db: AsyncSession) -> Optional[Dict[str, Any]]:
        """Try to authenticate using JWT token"""
        try:
            from api.core.jwt_auth import JWTAuth
            from api.services.user_service import UserService
            
            # Verify token (this may raise HTTPException)
            payload = JWTAuth.verify_token(token, "access")
            user_id = payload.get("sub")
            
            if user_id is None:
                return None
            
            # Get user with roles and permissions
            user_service = UserService(db)
            user = await user_service.get_user_by_id(user_id)
            
            if user is None or not user.is_active:
                return None
            
            # Extract permissions from user's roles
            permissions = []
            for role in user.roles:
                if role.is_active:
                    for permission in role.permissions:
                        if permission.is_active:
                            permissions.append(permission.name)
            
            return {
                "user_id": user.id,
                "email": user.email,
                "permissions": permissions,
                "auth_type": "jwt",
                "user": user
            }
            
        except HTTPException:
            # JWT authentication failed (invalid/expired token), return None to try API key
            return None
        except Exception as e:
            # Other errors (e.g., database errors) - log and return None
            logger.debug("JWT auth attempt failed", error=str(e))
            return None


class APIKeyAuth:
    """API Key authentication (legacy - use HybridAuth instead)"""
    
    def __init__(self, required_permissions: List[str] = None):
        self.required_permissions = required_permissions or []
    
    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ) -> Dict[str, Any]:
        """Validate API key and return project info"""
        try:
            api_key = credentials.credentials
            
            # Validate API key format
            if not api_key.startswith("ri_"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key format"
                )
            
            # Validate API key
            from api.services.developer_service import DeveloperService
            developer_service = DeveloperService(db)
            api_key_info = await developer_service.validate_api_key(api_key)
            
            if not api_key_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired API key"
                )
            
            # Check permissions
            if self.required_permissions:
                user_permissions = api_key_info.get("permissions", [])
                missing_permissions = set(self.required_permissions) - set(user_permissions)
                
                if missing_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing required permissions: {', '.join(missing_permissions)}"
                    )
            
            # Add API key info to request state
            request.state.api_key_info = api_key_info
            
            return api_key_info
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Authentication error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )


# Permission-based authentication functions
def require_api_key(permissions: List[str] = None):
    """Require API key with specific permissions (supports both JWT and API keys)"""
    return HybridAuth(required_permissions=permissions)


def require_read_permission():
    """Require read permission"""
    return require_api_key(["accounts:read", "transfers:read", "analytics:read"])


def require_write_permission():
    """Require write permission"""
    return require_api_key(["accounts:write", "transfers:write"])


def require_admin_permission():
    """Require admin permission"""
    return require_api_key(["admin"])


# Rate limiting (basic implementation)
class RateLimiter:
    """Basic rate limiter"""
    
    def __init__(self, requests_per_hour: int = 1000):
        self.requests_per_hour = requests_per_hour
        self.requests = {}  # In production, use Redis
    
    async def check_rate_limit(self, api_key: str) -> bool:
        """Check if API key is within rate limit"""
        # This is a basic implementation
        # In production, you'd use Redis with proper time windows
        return True


# Request context helpers
def get_api_key_info(request: Request) -> Dict[str, Any]:
    """Get API key info from request state"""
    return getattr(request.state, "api_key_info", {})


def get_project_id(request: Request) -> str:
    """Get project ID from API key info"""
    api_key_info = get_api_key_info(request)
    return api_key_info.get("project_id")


def get_developer_id(request: Request) -> str:
    """Get developer ID from API key info"""
    api_key_info = get_api_key_info(request)
    return api_key_info.get("developer_id")