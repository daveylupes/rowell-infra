"""
Transfer endpoints for unified Stellar and Hedera transfers
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import structlog

from api.core.database import get_db
from api.core.auth import require_api_key
from api.services.transfer_service import TransferService
from api.models.transaction import Transaction

logger = structlog.get_logger()
router = APIRouter()


# Pydantic models for request/response
class TransferRequest(BaseModel):
    """Request model for creating a transfer"""
    from_account: str = Field(..., description="Source account ID")
    to_account: str = Field(..., description="Destination account ID")
    asset_code: str = Field(..., description="Asset code (e.g., 'USDC', 'XLM', 'HBAR')")
    asset_issuer: Optional[str] = Field(None, description="Asset issuer (for Stellar assets)")
    amount: str = Field(..., description="Amount to transfer")
    network: str = Field(..., description="Network: 'stellar' or 'hedera'")
    environment: str = Field(..., description="Environment: 'testnet' or 'mainnet'")
    memo: Optional[str] = Field(None, description="Transaction memo")
    from_country: Optional[str] = Field(None, description="Source country code")
    to_country: Optional[str] = Field(None, description="Destination country code")
    metadata: Optional[dict] = Field(None, description="Additional transfer metadata")


class TransferResponse(BaseModel):
    """Response model for transfer information"""
    id: str
    transaction_hash: str
    network: str
    environment: str
    transaction_type: str
    status: str
    from_account: Optional[str]
    to_account: Optional[str]
    asset_code: str
    asset_issuer: Optional[str]
    amount: str
    amount_usd: Optional[str]
    from_country: Optional[str]
    to_country: Optional[str]
    from_region: Optional[str]
    to_region: Optional[str]
    memo: Optional[str]
    fee: Optional[str]
    fee_usd: Optional[str]
    created_at: str
    updated_at: str
    ledger_time: Optional[str]
    compliance_status: str
    risk_score: Optional[float]


class TransferStatusResponse(BaseModel):
    """Response model for comprehensive transfer status"""
    id: str
    transaction_hash: str
    status: str
    compliance_status: str
    risk_score: Optional[float]
    ledger_time: Optional[str]
    events: List[dict]
    blockchain_details: Optional[dict]
    fees: Optional[dict]
    compliance: Optional[dict]
    from_account: str
    to_account: str
    asset_code: str
    amount: str
    network: str
    environment: str
    created_at: str
    updated_at: str


class TransferListResponse(BaseModel):
    """Response model for paginated transfer listing"""
    transfers: List[TransferResponse]
    pagination: dict
    filters: dict
    sorting: dict


@router.post("/create", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
async def create_transfer(
    request: TransferRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["transfers:write"]))
):
    """Create a new transfer between accounts"""
    try:
        logger.info(
            "Creating transfer",
            from_account=request.from_account,
            to_account=request.to_account,
            asset_code=request.asset_code,
            amount=request.amount,
            network=request.network
        )
        
        transfer_service = TransferService(db)
        
        # Create the transfer
        transfer = await transfer_service.create_transfer(
            from_account=request.from_account,
            to_account=request.to_account,
            asset_code=request.asset_code,
            asset_issuer=request.asset_issuer,
            amount=request.amount,
            network=request.network,
            environment=request.environment,
            memo=request.memo,
            from_country=request.from_country,
            to_country=request.to_country,
            metadata=request.metadata,
            api_key=auth.get("api_key")
        )
        
        # For MVP, we'll skip background processing
        # background_tasks.add_task(
        #     transfer_service.submit_transfer,
        #     transfer.id
        # )
        
        logger.info("Transfer created successfully", transaction_hash=transfer.transaction_hash)
        
        return TransferResponse(
            id=str(transfer.id),
            transaction_hash=transfer.transaction_hash,
            network=transfer.network,
            environment=transfer.environment,
            transaction_type=transfer.transaction_type,
            status=transfer.status,
            from_account=transfer.from_account,
            to_account=transfer.to_account,
            asset_code=transfer.asset_code,
            asset_issuer=transfer.asset_issuer,
            amount=transfer.amount,
            amount_usd=transfer.amount_usd,
            from_country=transfer.from_country,
            to_country=transfer.to_country,
            from_region=transfer.from_region,
            to_region=transfer.to_region,
            memo=transfer.memo,
            fee=transfer.fee,
            fee_usd=transfer.fee_usd,
            created_at=transfer.created_at.isoformat(),
            updated_at=transfer.updated_at.isoformat(),
            ledger_time=transfer.ledger_time.isoformat() if transfer.ledger_time else None,
            compliance_status=transfer.compliance_status,
            risk_score=float(transfer.risk_score) if transfer.risk_score else None
        )
        
    except Exception as e:
        logger.error("Failed to create transfer", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transfer: {str(e)}"
        )


@router.get("/{transaction_hash}", response_model=TransferResponse)
async def get_transfer(
    transaction_hash: str,
    db: AsyncSession = Depends(get_db)
):
    """Get transfer information by transaction hash"""
    try:
        transfer_service = TransferService(db)
        transfer = await transfer_service.get_transfer(transaction_hash)
        
        if not transfer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transfer not found"
            )
        
        return TransferResponse(
            id=str(transfer.id),
            transaction_hash=transfer.transaction_hash,
            network=transfer.network,
            environment=transfer.environment,
            transaction_type=transfer.transaction_type,
            status=transfer.status,
            from_account=transfer.from_account,
            to_account=transfer.to_account,
            asset_code=transfer.asset_code,
            asset_issuer=transfer.asset_issuer,
            amount=transfer.amount,
            amount_usd=transfer.amount_usd,
            from_country=transfer.from_country,
            to_country=transfer.to_country,
            from_region=transfer.from_region,
            to_region=transfer.to_region,
            memo=transfer.memo,
            fee=transfer.fee,
            fee_usd=transfer.fee_usd,
            created_at=transfer.created_at.isoformat(),
            updated_at=transfer.updated_at.isoformat(),
            ledger_time=transfer.ledger_time.isoformat() if transfer.ledger_time else None,
            compliance_status=transfer.compliance_status,
            risk_score=float(transfer.risk_score) if transfer.risk_score else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get transfer", transaction_hash=transaction_hash, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transfer: {str(e)}"
        )


@router.get("/{transfer_id}/status", response_model=TransferStatusResponse)
async def get_transfer_status(
    transfer_id: str,
    include_events: bool = True,
    include_fees: bool = True,
    include_compliance: bool = True,
    refresh_blockchain: bool = False,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["transfers:read"]))
):
    """Get comprehensive transfer status and details (AC1-10)"""
    try:
        transfer_service = TransferService(db)
        status_info = await transfer_service.get_transfer_status(
            transfer_id=transfer_id,
            include_events=include_events,
            include_fees=include_fees,
            include_compliance=include_compliance,
            refresh_blockchain=refresh_blockchain
        )
        
        if not status_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transfer not found"
            )
        
        return TransferStatusResponse(
            id=status_info["id"],
            transaction_hash=status_info["transaction_hash"],
            status=status_info["status"],
            compliance_status=status_info["compliance_status"],
            risk_score=status_info["risk_score"],
            ledger_time=status_info["ledger_time"],
            events=status_info.get("events", []),
            blockchain_details=status_info.get("blockchain_details"),
            fees=status_info.get("fees"),
            compliance=status_info.get("compliance"),
            from_account=status_info["from_account"],
            to_account=status_info["to_account"],
            asset_code=status_info["asset_code"],
            amount=status_info["amount"],
            network=status_info["network"],
            environment=status_info["environment"],
            created_at=status_info["created_at"],
            updated_at=status_info["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get transfer status", transfer_id=transfer_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transfer status: {str(e)}"
        )


@router.get("/", response_model=TransferListResponse)
async def list_transfers(
    from_account: Optional[str] = None,
    to_account: Optional[str] = None,
    network: Optional[str] = None,
    environment: Optional[str] = None,
    asset_code: Optional[str] = None,
    transfer_status: Optional[str] = None,
    from_country: Optional[str] = None,
    to_country: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    include_fees: bool = True,
    include_compliance: bool = True,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["transfers:read"]))
):
    """List transfers with comprehensive filtering, pagination, and sorting (AC1-10)"""
    try:
        # Validate parameters
        if limit > 1000:
            limit = 1000  # Cap limit for performance
        if limit < 1:
            limit = 1
        
        if offset < 0:
            offset = 0
        
        valid_sort_fields = ["created_at", "updated_at", "amount", "status", "network"]
        if sort_by not in valid_sort_fields:
            sort_by = "created_at"
        
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        transfer_service = TransferService(db)
        result = await transfer_service.list_transfers(
            from_account=from_account,
            to_account=to_account,
            network=network,
            environment=environment,
            asset_code=asset_code,
            status=transfer_status,
            from_country=from_country,
            to_country=to_country,
            limit=limit,
            skip=offset,
            sort_by=sort_by,
            sort_order=sort_order,
            include_fees=include_fees,
            include_compliance=include_compliance
        )
        
        return TransferListResponse(**result)
        
    except Exception as e:
        logger.error("Failed to list transfers", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list transfers: {str(e)}"
        )


@router.post("/{transaction_hash}/retry")
async def retry_transfer(
    transaction_hash: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Retry a failed transfer"""
    try:
        transfer_service = TransferService(db)
        result = await transfer_service.retry_transfer(transaction_hash)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transfer not found or cannot be retried"
            )
        
        # Submit retry in background
        background_tasks.add_task(
            transfer_service.submit_transfer,
            result["transfer_id"]
        )
        
        return {"message": "Transfer retry initiated", "transaction_hash": transaction_hash}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retry transfer", transaction_hash=transaction_hash, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retry transfer: {str(e)}"
        )
