"""
Authentication API endpoints
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.database import get_db
from api.core.jwt_auth import get_current_user, get_current_active_user
from api.services.user_service import UserService
from api.schemas.user import (
    UserCreate, UserLogin, UserResponse, TokenResponse, 
    PasswordChange, PasswordResetRequest, PasswordReset,
    EmailVerificationRequest
)
from api.models.user import User
import structlog

logger = structlog.get_logger()
router = APIRouter(tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user and auto-login"""
    try:
        user_service = UserService(db)
        
        # Create user (returns user with roles already loaded)
        user = await user_service.create_user(user_data)
        
        # Get client IP and user agent
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Extract role names while database session is still active
        # Access relationships in async context before session closes
        try:
            roles_list = list(user.roles) if user.roles else []
            role_names = [r.name for r in roles_list]
            # Force access to permissions to ensure they're loaded
            for role in roles_list:
                _ = list(role.permissions) if role.permissions else []
        except Exception as e:
            logger.warning("Could not access roles, using empty list", error=str(e))
            role_names = []
        
        # Auto-login: Create session and tokens (pass role names to avoid lazy loading)
        tokens = await user_service.create_user_session(user, ip_address, user_agent, role_names=role_names)
        
        logger.info(
            "User registered and auto-logged in",
            user_id=user.id,
            email=user.email,
            ip_address=ip_address
        )
        
        # Access relationships in async context before serialization
        # This prevents "greenlet_spawn" errors during Pydantic validation
        roles_list = list(user.roles) if user.roles else []
        for role in roles_list:
            permissions_list = list(role.permissions) if role.permissions else []
            _ = permissions_list  # Force access in async context
        
        # Return user data with tokens (for auto-login)
        user_response = UserResponse.model_validate(user)
        
        return {
            "user": user_response.model_dump(),
            "tokens": {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "bearer",
                "expires_in": 900
            }
        }
        
    except ValueError as e:
        error_msg = str(e)
        logger.error("Registration failed - validation error", error=error_msg, email=user_data.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error("Registration failed", error=str(e), email=user_data.email, traceback=error_trace)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Login user and return tokens"""
    try:
        user_service = UserService(db)
        
        # Authenticate user
        user = await user_service.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is verified (disabled for presentation)
        # if not user.is_verified:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Email not verified. Please check your email for verification link."
        #     )
        
        # Get client IP and user agent
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Create session and tokens
        tokens = await user_service.create_user_session(user, ip_address, user_agent)
        
        logger.info(
            "User logged in successfully",
            user_id=user.id,
            email=user.email,
            ip_address=ip_address
        )
        
        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type="bearer",
            expires_in=900  # 15 minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e), email=login_data.email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: Dict[str, str],
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        refresh_token = refresh_data.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )
        
        user_service = UserService(db)
        tokens = await user_service.refresh_user_session(refresh_token)
        
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type="bearer",
            expires_in=900  # 15 minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout_user(
    refresh_data: Dict[str, str],
    db: AsyncSession = Depends(get_db)
):
    """Logout user and revoke session"""
    try:
        refresh_token = refresh_data.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )
        
        user_service = UserService(db)
        success = await user_service.revoke_user_session(refresh_token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to logout"
            )
        
        return {"message": "Logged out successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information with roles and permissions loaded"""
    # Ensure roles and permissions are explicitly loaded
    from api.services.user_service import UserService
    user_service = UserService(db)
    
    # Get fresh user data with roles and permissions loaded
    user_with_roles = await user_service.get_user_by_id(current_user.id)
    if not user_with_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Access relationships to ensure they're loaded before serialization
    # This prevents lazy loading issues when serializing
    roles_list = list(user_with_roles.roles) if user_with_roles.roles else []
    for role in roles_list:
        permissions_list = list(role.permissions) if role.permissions else []
        _ = permissions_list  # Force access
    
    # Explicitly convert to Pydantic model to ensure serialization
    # Use model_validate with from_attributes=True
    user_response = UserResponse.model_validate(user_with_roles)
    
    logger.info(
        "User info retrieved",
        user_id=user_with_roles.id,
        roles_count=len(roles_list),
        role_names=[r.name for r in roles_list],
        permissions_count=sum(len(r.permissions) for r in roles_list)
    )
    
    return user_response


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information"""
    try:
        user_service = UserService(db)
        updated_user = await user_service.update_user(current_user.id, user_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user"
            )
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("User update failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User update failed"
        )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    try:
        user_service = UserService(db)
        success = await user_service.change_password(
            current_user.id,
            password_data.old_password,
            password_data.new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid old password"
            )
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Password change failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.post("/verify-email")
async def verify_email(
    verification_data: EmailVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Verify user email with token"""
    try:
        user_service = UserService(db)
        success = await user_service.verify_email(verification_data.token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Email verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/request-password-reset")
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset token"""
    try:
        user_service = UserService(db)
        token = await user_service.create_password_reset(reset_data.email)
        
        # Always return success to prevent email enumeration
        return {"message": "If the email exists, a password reset link has been sent"}
        
    except Exception as e:
        logger.error("Password reset request failed", error=str(e), email=reset_data.email)
        # Always return success to prevent email enumeration
        return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """Reset password with token"""
    try:
        user_service = UserService(db)
        success = await user_service.reset_password(reset_data.token, reset_data.new_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Password reset failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
