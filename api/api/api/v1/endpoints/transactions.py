"""
Transaction endpoints for querying and monitoring
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, Field
import structlog

from api.core.database import get_db
from api.services.transaction_service import TransactionService

logger = structlog.get_logger()
router = APIRouter()


# Pydantic models for request/response
class TransactionResponse(BaseModel):
    """Response model for transaction information"""
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
    compliance_flags: Optional[dict]


class TransactionEventResponse(BaseModel):
    """Response model for transaction events"""
    id: str
    transaction_id: str
    transaction_hash: str
    event_type: str
    event_data: Optional[dict]
    network: str
    environment: str
    created_at: str
    blockchain_timestamp: Optional[str]


@router.get("/{transaction_hash}", response_model=TransactionResponse)
async def get_transaction(
    transaction_hash: str,
    db: AsyncSession = Depends(get_db)
):
    """Get transaction information by hash"""
    try:
        transaction_service = TransactionService(db)
        transaction = await transaction_service.get_transaction(transaction_hash)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return TransactionResponse(
            id=str(transaction.id),
            transaction_hash=transaction.transaction_hash,
            network=transaction.network,
            environment=transaction.environment,
            transaction_type=transaction.transaction_type,
            status=transaction.status,
            from_account=transaction.from_account,
            to_account=transaction.to_account,
            asset_code=transaction.asset_code,
            asset_issuer=transaction.asset_issuer,
            amount=transaction.amount,
            amount_usd=transaction.amount_usd,
            from_country=transaction.from_country,
            to_country=transaction.to_country,
            from_region=transaction.from_region,
            to_region=transaction.to_region,
            memo=transaction.memo,
            fee=transaction.fee,
            fee_usd=transaction.fee_usd,
            created_at=transaction.created_at.isoformat(),
            updated_at=transaction.updated_at.isoformat(),
            ledger_time=transaction.ledger_time.isoformat() if transaction.ledger_time else None,
            compliance_status=transaction.compliance_status,
            risk_score=float(transaction.risk_score) if transaction.risk_score else None,
            compliance_flags=transaction.compliance_flags
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get transaction", transaction_hash=transaction_hash, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transaction: {str(e)}"
        )


@router.get("/{transaction_hash}/events", response_model=List[TransactionEventResponse])
async def get_transaction_events(
    transaction_hash: str,
    db: AsyncSession = Depends(get_db)
):
    """Get transaction events by hash"""
    try:
        transaction_service = TransactionService(db)
        events = await transaction_service.get_transaction_events(transaction_hash)
        
        return [
            TransactionEventResponse(
                id=str(event.id),
                transaction_id=str(event.transaction_id),
                transaction_hash=event.transaction_hash,
                event_type=event.event_type,
                event_data=event.event_data,
                network=event.network,
                environment=event.environment,
                created_at=event.created_at.isoformat(),
                blockchain_timestamp=event.blockchain_timestamp.isoformat() if event.blockchain_timestamp else None
            )
            for event in events
        ]
        
    except Exception as e:
        logger.error("Failed to get transaction events", transaction_hash=transaction_hash, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transaction events: {str(e)}"
        )


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    from_account: Optional[str] = None,
    to_account: Optional[str] = None,
    network: Optional[str] = None,
    environment: Optional[str] = None,
    transaction_type: Optional[str] = None,
    status: Optional[str] = None,
    asset_code: Optional[str] = None,
    from_country: Optional[str] = None,
    to_country: Optional[str] = None,
    from_region: Optional[str] = None,
    to_region: Optional[str] = None,
    compliance_status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List transactions with optional filtering"""
    try:
        transaction_service = TransactionService(db)
        transactions = await transaction_service.list_transactions(
            from_account=from_account,
            to_account=to_account,
            network=network,
            environment=environment,
            transaction_type=transaction_type,
            status=status,
            asset_code=asset_code,
            from_country=from_country,
            to_country=to_country,
            from_region=from_region,
            to_region=to_region,
            compliance_status=compliance_status,
            limit=limit,
            offset=offset
        )
        
        return [
            TransactionResponse(
                id=str(transaction.id),
                transaction_hash=transaction.transaction_hash,
                network=transaction.network,
                environment=transaction.environment,
                transaction_type=transaction.transaction_type,
                status=transaction.status,
                from_account=transaction.from_account,
                to_account=transaction.to_account,
                asset_code=transaction.asset_code,
                asset_issuer=transaction.asset_issuer,
                amount=transaction.amount,
                amount_usd=transaction.amount_usd,
                from_country=transaction.from_country,
                to_country=transaction.to_country,
                from_region=transaction.from_region,
                to_region=transaction.to_region,
                memo=transaction.memo,
                fee=transaction.fee,
                fee_usd=transaction.fee_usd,
                created_at=transaction.created_at.isoformat(),
                updated_at=transaction.updated_at.isoformat(),
                ledger_time=transaction.ledger_time.isoformat() if transaction.ledger_time else None,
                compliance_status=transaction.compliance_status,
                risk_score=float(transaction.risk_score) if transaction.risk_score else None,
                compliance_flags=transaction.compliance_flags
            )
            for transaction in transactions
        ]
        
    except Exception as e:
        logger.error("Failed to list transactions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list transactions: {str(e)}"
        )


@router.get("/account/{account_id}", response_model=List[TransactionResponse])
async def get_account_transactions(
    account_id: str,
    network: Optional[str] = None,
    environment: Optional[str] = None,
    transaction_type: Optional[str] = None,
    status: Optional[str] = None,
    asset_code: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get transactions for a specific account"""
    try:
        transaction_service = TransactionService(db)
        transactions = await transaction_service.get_account_transactions(
            account_id=account_id,
            network=network,
            environment=environment,
            transaction_type=transaction_type,
            status=status,
            asset_code=asset_code,
            limit=limit,
            offset=offset
        )
        
        return [
            TransactionResponse(
                id=str(transaction.id),
                transaction_hash=transaction.transaction_hash,
                network=transaction.network,
                environment=transaction.environment,
                transaction_type=transaction.transaction_type,
                status=transaction.status,
                from_account=transaction.from_account,
                to_account=transaction.to_account,
                asset_code=transaction.asset_code,
                asset_issuer=transaction.asset_issuer,
                amount=transaction.amount,
                amount_usd=transaction.amount_usd,
                from_country=transaction.from_country,
                to_country=transaction.to_country,
                from_region=transaction.from_region,
                to_region=transaction.to_region,
                memo=transaction.memo,
                fee=transaction.fee,
                fee_usd=transaction.fee_usd,
                created_at=transaction.created_at.isoformat(),
                updated_at=transaction.updated_at.isoformat(),
                ledger_time=transaction.ledger_time.isoformat() if transaction.ledger_time else None,
                compliance_status=transaction.compliance_status,
                risk_score=float(transaction.risk_score) if transaction.risk_score else None,
                compliance_flags=transaction.compliance_flags
            )
            for transaction in transactions
        ]
        
    except Exception as e:
        logger.error("Failed to get account transactions", account_id=account_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get account transactions: {str(e)}"
        )


@router.get("/corridor/{from_country}/{to_country}", response_model=List[TransactionResponse])
async def get_corridor_transactions(
    from_country: str,
    to_country: str,
    asset_code: Optional[str] = None,
    network: Optional[str] = None,
    environment: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get transactions for a specific corridor (country to country)"""
    try:
        transaction_service = TransactionService(db)
        transactions = await transaction_service.get_corridor_transactions(
            from_country=from_country,
            to_country=to_country,
            asset_code=asset_code,
            network=network,
            environment=environment,
            limit=limit,
            offset=offset
        )
        
        return [
            TransactionResponse(
                id=str(transaction.id),
                transaction_hash=transaction.transaction_hash,
                network=transaction.network,
                environment=transaction.environment,
                transaction_type=transaction.transaction_type,
                status=transaction.status,
                from_account=transaction.from_account,
                to_account=transaction.to_account,
                asset_code=transaction.asset_code,
                asset_issuer=transaction.asset_issuer,
                amount=transaction.amount,
                amount_usd=transaction.amount_usd,
                from_country=transaction.from_country,
                to_country=transaction.to_country,
                from_region=transaction.from_region,
                to_region=transaction.to_region,
                memo=transaction.memo,
                fee=transaction.fee,
                fee_usd=transaction.fee_usd,
                created_at=transaction.created_at.isoformat(),
                updated_at=transaction.updated_at.isoformat(),
                ledger_time=transaction.ledger_time.isoformat() if transaction.ledger_time else None,
                compliance_status=transaction.compliance_status,
                risk_score=float(transaction.risk_score) if transaction.risk_score else None,
                compliance_flags=transaction.compliance_flags
            )
            for transaction in transactions
        ]
        
    except Exception as e:
        logger.error("Failed to get corridor transactions", from_country=from_country, to_country=to_country, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get corridor transactions: {str(e)}"
        )
