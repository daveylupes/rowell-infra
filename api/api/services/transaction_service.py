"""
Transaction service for handling transaction operations
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from api.models.transaction import Transaction
from api.schemas.transaction import TransactionCreate, TransactionResponse
import structlog

logger = structlog.get_logger()


class TransactionService:
    """Service for managing transactions"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction"""
        # Placeholder implementation
        pass
    
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        try:
            result = await self.db.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Failed to get transaction", transaction_id=transaction_id, error=str(e))
            return None
    
    async def list_transactions(
        self,
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
        offset: int = 0
    ) -> List[Transaction]:
        """List transactions with optional filtering"""
        try:
            query = select(Transaction)
            
            # Build filters
            filters = []
            
            if from_account:
                filters.append(Transaction.from_account == from_account)
            if to_account:
                filters.append(Transaction.to_account == to_account)
            if network:
                filters.append(Transaction.network == network)
            if environment:
                filters.append(Transaction.environment == environment)
            if transaction_type:
                filters.append(Transaction.transaction_type == transaction_type)
            if status:
                filters.append(Transaction.status == status)
            if asset_code:
                filters.append(Transaction.asset_code == asset_code)
            if from_country:
                filters.append(Transaction.from_country == from_country)
            if to_country:
                filters.append(Transaction.to_country == to_country)
            if from_region:
                filters.append(Transaction.from_region == from_region)
            if to_region:
                filters.append(Transaction.to_region == to_region)
            if compliance_status:
                filters.append(Transaction.compliance_status == compliance_status)
            
            # Apply filters
            if filters:
                query = query.where(and_(*filters))
            
            # Order by created_at descending (newest first)
            query = query.order_by(Transaction.created_at.desc())
            
            # Pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            return list(result.scalars().all())
            
        except Exception as e:
            logger.error("Failed to list transactions", error=str(e), exc_info=True)
            raise
    
    async def get_account_transactions(
        self,
        account_id: str,
        network: Optional[str] = None,
        environment: Optional[str] = None,
        transaction_type: Optional[str] = None,
        status: Optional[str] = None,
        asset_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Transaction]:
        """Get transactions for a specific account"""
        try:
            query = select(Transaction).where(
                or_(
                    Transaction.from_account == account_id,
                    Transaction.to_account == account_id
                )
            )
            
            # Additional filters
            if network:
                query = query.where(Transaction.network == network)
            if environment:
                query = query.where(Transaction.environment == environment)
            if transaction_type:
                query = query.where(Transaction.transaction_type == transaction_type)
            if status:
                query = query.where(Transaction.status == status)
            if asset_code:
                query = query.where(Transaction.asset_code == asset_code)
            
            query = query.order_by(Transaction.created_at.desc())
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            return list(result.scalars().all())
            
        except Exception as e:
            logger.error("Failed to get account transactions", account_id=account_id, error=str(e))
            raise
