"""
Account management endpoints for Stellar and Hedera
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import structlog

from api.core.database import get_db
from api.core.auth import require_api_key, get_project_id
from api.services.account_service import AccountService
from api.services.key_storage_service import KeyStorageService
from api.models.account import Account, AccountBalance

logger = structlog.get_logger()
router = APIRouter()


# Pydantic models for request/response
class AccountCreateRequest(BaseModel):
    """Request model for creating a new account"""
    network: str = Field(..., description="Network: 'stellar' or 'hedera'")
    environment: str = Field(..., description="Environment: 'testnet' or 'mainnet'")
    account_type: str = Field(..., description="Account type: 'user', 'merchant', 'anchor', 'ngo'")
    country_code: Optional[str] = Field(None, description="ISO country code (e.g., 'KE', 'NG')")
    region: Optional[str] = Field(None, description="Region: 'east_africa', 'west_africa', etc.")
    metadata: Optional[dict] = Field(None, description="Additional account metadata")


class AccountResponse(BaseModel):
    """Response model for account information"""
    id: str
    account_id: str
    network: str
    environment: str
    account_type: str
    country_code: Optional[str]
    region: Optional[str]
    is_active: bool
    is_verified: bool
    is_compliant: bool
    kyc_status: str
    created_at: str
    updated_at: str
    last_activity: Optional[str]
    metadata: Optional[dict]
    # Security: Private key is NOT included here
    key_retrieval_token: Optional[str] = None  # Only present on account creation
    key_retrieval_url: Optional[str] = None  # Only present on account creation
    security_warning: Optional[str] = None  # Only present on account creation


class AccountBalanceResponse(BaseModel):
    """Response model for account balance"""
    account_id: str
    network: str
    asset_code: str
    asset_issuer: Optional[str]
    balance: str
    balance_usd: Optional[str]
    updated_at: str


@router.post("/create", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    request: AccountCreateRequest,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["accounts:write"]))
):
    """Create a new account on Stellar or Hedera network"""
    try:
        # Rate limiting is handled by the auth middleware
        
        logger.info("Creating new account", network=request.network, environment=request.environment)
        
        account_service = AccountService(db)
        account_data = await account_service.create_account(
            network=request.network,
            environment=request.environment,
            account_type=request.account_type,
            country_code=request.country_code,
            region=request.region,
            metadata=request.metadata,
            project_id=auth.get("project_id")
        )
        
        logger.info("Account created successfully", account_id=account_data["account_id"])
        
        return AccountResponse(**account_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create account", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create account: {str(e)}"
        )


@router.get("/", response_model=Dict[str, Any])
async def list_accounts(
    network: Optional[str] = None,
    environment: Optional[str] = None,
    account_type: Optional[str] = None,
    country_code: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    include_balances: bool = False,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["accounts:read"]))
):
    """List accounts with pagination and filtering (AC1-10)"""
    try:
        # Validate parameters (AC5)
        if limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 1000"
            )
        if offset < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Offset must be non-negative"
            )
        if network and network.lower() not in ["stellar", "hedera"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Network must be 'stellar' or 'hedera'"
            )
        if environment and environment.lower() not in ["testnet", "mainnet"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Environment must be 'testnet' or 'mainnet'"
            )
        if account_type and account_type.lower() not in ["user", "merchant", "anchor", "ngo"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account type must be 'user', 'merchant', 'anchor', or 'ngo'"
            )
        
        account_service = AccountService(db)
        
        # For JWT users without project_id, we need a different approach to filter accounts
        # We'll use user_id from auth if available (for JWT users)
        user_id = None
        if auth.get("auth_type") == "jwt":
            user_id = auth.get("user_id")
        
        result = await account_service.list_accounts(
            project_id=auth.get("project_id"),
            user_id=user_id,
            network=network,
            environment=environment,
            account_type=account_type,
            country_code=country_code,
            limit=limit,
            offset=offset,
            include_balances=include_balances
        )
        
        # Convert accounts to response format
        accounts_response = []
        for account in result["accounts"]:
            account_response = AccountResponse(
                id=account["id"],
                account_id=account["account_id"],
                network=account["network"],
                environment=account["environment"],
                account_type=account["account_type"],
                country_code=account["country_code"],
                region=account["region"],
                is_active=account["is_active"],
                is_verified=account["is_verified"],
                is_compliant=account["is_compliant"],
                kyc_status=account["kyc_status"],
                created_at=account["created_at"],
                updated_at=account["updated_at"],
                last_activity=account["last_activity"],
                metadata=account["metadata"]
            )
            accounts_response.append(account_response)
        
        return {
            "accounts": accounts_response,
            "pagination": result["pagination"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list accounts", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list accounts: {str(e)}"
        )


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get basic account information by account ID"""
    try:
        account_service = AccountService(db)
        account = await account_service.get_account(account_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        return AccountResponse(**account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get account", account_id=account_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get account: {str(e)}"
        )


@router.get("/{account_id}/details")
async def get_account_details(
    account_id: str,
    include_balances: bool = True,
    include_transactions: bool = True,
    include_compliance: bool = True,
    transaction_limit: int = 10,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["accounts:read"]))
):
    """Get comprehensive account details (AC1-9)"""
    try:
        # Validate parameters (AC5)
        if transaction_limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction limit cannot exceed 100"
            )
        if transaction_limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction limit must be at least 1"
            )
        
        account_service = AccountService(db)
        account_details = await account_service.get_account_details(
            account_id=account_id,
            include_balances=include_balances,
            include_transactions=include_transactions,
            include_compliance=include_compliance,
            transaction_limit=transaction_limit
        )
        
        if not account_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        return account_details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get account details", account_id=account_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get account details: {str(e)}"
        )


@router.get("/{account_id}/balances", response_model=List[AccountBalanceResponse])
async def get_account_balances(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get account balances for all assets"""
    try:
        account_service = AccountService(db)
        
        # Get account info first to know the network and blockchain account_id
        account = await account_service.get_account(account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Get balances from blockchain
        balances = await account_service.get_account_balances(account_id)
        
        return [
            AccountBalanceResponse(
                account_id=account["account_id"],  # Use blockchain account_id, not internal UUID
                network=account["network"],  # Get network from account data
                asset_code=balance["asset_code"],
                asset_issuer=balance.get("asset_issuer"),
                balance=balance["balance"],
                balance_usd=balance.get("balance_usd"),
                updated_at=datetime.now().isoformat()
            )
            for balance in balances
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get account balances", account_id=account_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get account balances: {str(e)}"
        )


class KeyRetrievalRequest(BaseModel):
    """Request model for retrieving private key"""
    token: str = Field(..., description="One-time token from account creation")


class KeyRetrievalResponse(BaseModel):
    """Response model for private key retrieval"""
    account_id: str
    private_key: str
    network: str
    warning: str = "⚠️ SECURITY WARNING: Store this key securely. It cannot be recovered. Never share it or commit it to version control."


@router.post("/{account_id}/key", response_model=KeyRetrievalResponse, status_code=status.HTTP_200_OK)
async def retrieve_account_key(
    account_id: str,
    request: KeyRetrievalRequest,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["accounts:read"]))
):
    """
    Retrieve private key securely using one-time token
    
    SECURITY: This endpoint returns the private key ONE TIME ONLY.
    The token expires after 30 minutes and can only be used once.
    """
    try:
        # Verify account exists and belongs to user
        account_service = AccountService(db)
        account = await account_service.get_account(account_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Verify account belongs to authenticated user's project (skip for JWT users without project_id)
        project_id = auth.get("project_id")
        if project_id and account.get("project_id") and account.get("project_id") != project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this account"
            )
        
        # Retrieve key using token
        key_storage = KeyStorageService(db)
        key_data = await key_storage.retrieve_key(request.token)
        
        if not key_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token. Private key can only be retrieved once using the token provided during account creation."
            )
        
        # Verify account ID matches - key_data has blockchain account_id
        blockchain_account_id = account.get("account_id")
        stored_account_id = key_data.get("account_id")
        if stored_account_id and blockchain_account_id and stored_account_id != blockchain_account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token does not match this account"
            )
        
        logger.warning(
            "Private key retrieved",
            account_id=blockchain_account_id,
            network=key_data["network"]
        )
        
        # Return blockchain account_id in response, not internal UUID
        return KeyRetrievalResponse(
            account_id=blockchain_account_id,  # Use blockchain account_id, not internal UUID
            private_key=key_data["private_key"],
            network=key_data["network"],
            warning="⚠️ SECURITY WARNING: Store this key securely. It cannot be recovered. Never share it or commit it to version control."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve account key", account_id=account_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve account key: {str(e)}"
        )




