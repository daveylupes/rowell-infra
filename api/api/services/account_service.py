"""
Account service for handling account operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from api.models.account import Account
from api.schemas.account import AccountCreate, AccountResponse
from api.services.stellar_service import StellarService
from api.services.key_storage_service import KeyStorageService
import structlog
import uuid
from datetime import datetime

logger = structlog.get_logger()


class AccountService:
    """Service for managing accounts"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_account(
        self, 
        network: str, 
        environment: str, 
        account_type: str, 
        country_code: str,
        region: Optional[str] = None,
        metadata: Optional[Dict] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new account on Stellar or Hedera network"""
        try:
            logger.info("Creating new account", network=network, environment=environment, account_type=account_type)
            
            # Initialize blockchain service
            if network.lower() == "stellar":
                blockchain_service = StellarService(environment)
            elif network.lower() == "hedera":
                from api.services.hedera_service import HederaService
                blockchain_service = HederaService(environment)
            else:
                raise ValueError(f"Unsupported network: {network}")
            
            # Create account on blockchain
            blockchain_account = await blockchain_service.create_account(
                account_type=account_type,
                metadata=metadata
            )
            
            # Create database record
            # Ensure account_id is a string (handle AccountId objects from Hedera SDK)
            account_id_str = blockchain_account["account_id"]
            if not isinstance(account_id_str, str):
                account_id_str = str(account_id_str)
            
            account = Account(
                account_id=account_id_str,
                network=network.lower(),
                environment=environment.lower(),
                account_type=account_type,
                country_code=country_code,
                region=region,
                account_metadata=metadata,
                project_id=project_id,
                is_active=True,
                is_verified=False,
                is_compliant=False,
                kyc_status="pending"
            )
            
            self.db.add(account)
            await self.db.commit()
            await self.db.refresh(account)
            
            logger.info("Account created successfully", account_id=account.account_id)
            
            # Get private/secret key from blockchain account
            private_key = blockchain_account.get("secret_key") or blockchain_account.get("private_key")
            
            # Store key securely and get one-time token
            key_storage = KeyStorageService(self.db)
            key_token = await key_storage.store_key(
                account_id=account.account_id,  # Use blockchain account_id for storage
                private_key=private_key,
                network=network.lower(),
                expires_in_minutes=30  # Token valid for 30 minutes
            )
            
            # Return account data WITHOUT private key
            # Key must be retrieved separately using secure endpoint
            return {
                "id": str(account.id),
                "account_id": account.account_id,
                # SECURITY: Private key NOT returned in response
                "key_retrieval_token": key_token,  # One-time token for secure key retrieval
                "key_retrieval_url": f"/api/v1/accounts/{account.id}/key",
                "network": account.network,
                "environment": account.environment,
                "account_type": account.account_type,
                "country_code": account.country_code,
                "region": account.region,
                "is_active": account.is_active,
                "is_verified": account.is_verified,
                "is_compliant": account.is_compliant,
                "kyc_status": account.kyc_status,
                "created_at": account.created_at.isoformat(),
                "updated_at": account.updated_at.isoformat(),
                "last_activity": account.last_activity.isoformat() if account.last_activity else None,
                "metadata": account.account_metadata,
                "security_warning": "Private key stored securely. Use key_retrieval_token to retrieve it once. Store it securely - it cannot be recovered."
            }
            
        except Exception as e:
            logger.error("Failed to create account", error=str(e))
            await self.db.rollback()
            raise

    async def list_accounts(
        self, 
        project_id: Optional[str] = None,
        user_id: Optional[str] = None,
        network: Optional[str] = None,
        environment: Optional[str] = None,
        account_type: Optional[str] = None,
        country_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        include_balances: bool = False
    ) -> Dict[str, Any]:
        """List accounts with pagination, filtering, and optional balance information (AC1-10)"""
        try:
            logger.info("Listing accounts with filters", 
                       project_id=project_id, user_id=user_id, network=network, environment=environment,
                       account_type=account_type, country_code=country_code,
                       limit=limit, offset=offset, include_balances=include_balances)
            
            # Build query with filters
            query = select(Account)
            count_query = select(func.count(Account.id))
            
            # Apply filters
            filters = []
            if project_id:
                # If project_id is provided, only show accounts for that project
                filters.append(Account.project_id == project_id)
            # Note: We no longer filter out accounts without project_id
            # This allows JWT-authenticated users to see their accounts even without a project_id
            
            # Filter out Stellar accounts - only show Hedera accounts
            # If network filter is provided and it's not "hedera", the query will return empty anyway
            if network:
                # Only allow Hedera network filter
                if network.lower() == "hedera":
                    filters.append(Account.network == "hedera")
                else:
                    # If user requests non-Hedera network, return empty (Stellar not supported)
                    filters.append(Account.network == "invalid_network")  # Will return no results
            else:
                # No network filter specified - default to Hedera only
                filters.append(Account.network == "hedera")
            if environment:
                filters.append(Account.environment == environment.lower())
            if account_type:
                filters.append(Account.account_type == account_type.lower())
            if country_code:
                filters.append(Account.country_code == country_code.upper())
            
            if filters:
                query = query.where(and_(*filters))
                count_query = count_query.where(and_(*filters))
            
            # Add pagination
            query = query.offset(offset).limit(limit)
            
            # Execute queries
            result = await self.db.execute(query)
            accounts = result.scalars().all()
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Process accounts
            account_list = []
            for account in accounts:
                # Sanitize account_id to handle any malformed entries
                account_id = account.account_id
                if isinstance(account_id, str) and account_id.startswith('<com.hedera'):
                    # Skip accounts with malformed Java object IDs
                    logger.warning("Skipping account with malformed ID", internal_id=account.id, bad_id=account_id[:100])
                    continue
                
                account_data = {
                    "id": str(account.id),
                    "account_id": account.account_id,
                    "network": account.network,
                    "environment": account.environment,
                    "account_type": account.account_type,
                    "country_code": account.country_code,
                    "region": account.region,
                    "is_active": account.is_active,
                    "is_verified": account.is_verified,
                    "is_compliant": account.is_compliant,
                    "kyc_status": account.kyc_status,
                    "metadata": account.account_metadata if account.account_metadata else {},
                    "created_at": account.created_at.isoformat(),
                    "updated_at": account.updated_at.isoformat() if account.updated_at else None,
                    "last_activity": account.last_activity.isoformat() if account.last_activity else None
                }
                
                # Add balance information if requested (AC4, AC10)
                if include_balances:
                    try:
                        balances = await self.get_account_balances(account.account_id)
                        account_data["balances"] = balances
                    except Exception as e:
                        logger.warning("Failed to get balances for account", 
                                     account_id=account.account_id, error=str(e))
                        account_data["balances"] = []
                
                account_list.append(account_data)
            
            return {
                "accounts": account_list,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total_count
                }
            }
            
        except Exception as e:
            logger.error("Failed to list accounts", 
                        project_id=project_id, network=network, environment=environment,
                        account_type=account_type, country_code=country_code,
                        error=str(e))
            raise
    
    async def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account by ID (internal database ID)"""
        try:
            result = await self.db.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            
            if not account:
                return None
            
            return {
                "id": str(account.id),
                "account_id": account.account_id,
                "network": account.network,
                "environment": account.environment,
                "account_type": account.account_type,
                "country_code": account.country_code,
                "region": account.region,
                "is_active": account.is_active,
                "is_verified": account.is_verified,
                "is_compliant": account.is_compliant,
                "kyc_status": account.kyc_status,
                "created_at": account.created_at.isoformat(),
                "updated_at": account.updated_at.isoformat(),
                "last_activity": account.last_activity.isoformat() if account.last_activity else None,
                "metadata": account.account_metadata
            }
            
        except Exception as e:
            logger.error("Failed to get account", account_id=account_id, error=str(e))
            raise
    
    async def get_account_details(
        self, 
        account_id: str, 
        include_balances: bool = True,
        include_transactions: bool = True,
        include_compliance: bool = True,
        transaction_limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Get comprehensive account details (AC1-9)"""
        try:
            logger.info("Getting comprehensive account details", 
                       account_id=account_id, include_balances=include_balances,
                       include_transactions=include_transactions, include_compliance=include_compliance)
            
            # Get basic account information
            account = await self.get_account(account_id)
            if not account:
                return None
            
            # Initialize result with basic account info
            result = account.copy()
            
            # Add real-time balance data (AC2, AC6)
            if include_balances:
                try:
                    balances = await self.get_account_balances(account_id)
                    result["balances"] = balances
                except Exception as e:
                    logger.warning("Failed to get account balances", 
                                 account_id=account_id, error=str(e))
                    result["balances"] = []
            
            # Add transaction history (AC3, AC7)
            if include_transactions:
                try:
                    transactions = await self.get_account_transactions(
                        account_id, limit=transaction_limit
                    )
                    result["recent_transactions"] = transactions
                except Exception as e:
                    logger.warning("Failed to get account transactions", 
                                 account_id=account_id, error=str(e))
                    result["recent_transactions"] = []
            
            # Add compliance status (AC4, AC8)
            if include_compliance:
                try:
                    compliance_info = await self.get_account_compliance(account_id)
                    result["compliance"] = compliance_info
                except Exception as e:
                    logger.warning("Failed to get compliance information", 
                                 account_id=account_id, error=str(e))
                    result["compliance"] = {
                        "kyc_status": account["kyc_status"],
                        "is_verified": account["is_verified"],
                        "is_compliant": account["is_compliant"],
                        "flags": [],
                        "last_verified": None
                    }
            
            return result
            
        except Exception as e:
            logger.error("Failed to get account details", account_id=account_id, error=str(e))
            raise
    
    async def get_account_transactions(
        self, 
        account_id: str, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get account transaction history (AC3, AC7)"""
        try:
            # Get account from database to determine network
            result = await self.db.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            
            if not account:
                raise ValueError(f"Account not found: {account_id}")
            
            # Initialize blockchain service
            if account.network.lower() == "stellar":
                blockchain_service = StellarService(account.environment)
            elif account.network.lower() == "hedera":
                from api.services.hedera_service import HederaService
                blockchain_service = HederaService(account.environment)
            else:
                raise ValueError(f"Unsupported network: {account.network}")
            
            # Get transactions from blockchain
            transactions = await blockchain_service.get_account_transactions(
                account.account_id, limit=limit, offset=offset
            )
            
            return transactions
            
        except Exception as e:
            logger.error("Failed to get account transactions", 
                        account_id=account_id, error=str(e))
            raise
    
    async def get_account_compliance(self, account_id: str) -> Dict[str, Any]:
        """Get account compliance information (AC4, AC8)"""
        try:
            # Get account from database
            result = await self.db.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            
            if not account:
                raise ValueError(f"Account not found: {account_id}")
            
            # For MVP, return basic compliance info from account record
            # In production, this would integrate with a dedicated compliance service
            return {
                "kyc_status": account.kyc_status,
                "is_verified": account.is_verified,
                "is_compliant": account.is_compliant,
                "flags": [],  # Would be populated from compliance service
                "last_verified": account.updated_at.isoformat() if account.updated_at else None,
                "verification_level": "basic",  # Would be determined by compliance service
                "risk_score": 0.0  # Would be calculated by compliance service
            }
            
        except Exception as e:
            logger.error("Failed to get account compliance", 
                        account_id=account_id, error=str(e))
            raise
    
    async def get_account_balances(self, account_id: str) -> List[Dict[str, Any]]:
        """Get account balances from blockchain"""
        try:
            # Get account from database
            result = await self.db.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            
            if not account:
                raise ValueError(f"Account not found: {account_id}")
            
            # Initialize blockchain service
            if account.network.lower() == "stellar":
                blockchain_service = StellarService(account.environment)
            elif account.network.lower() == "hedera":
                from api.services.hedera_service import HederaService
                blockchain_service = HederaService(account.environment)
            else:
                raise ValueError(f"Unsupported network: {account.network}")
            
            # Get balances from blockchain
            balances = await blockchain_service.get_account_balances(account.account_id)
            
            return balances
            
        except Exception as e:
            logger.error("Failed to get account balances", account_id=account_id, error=str(e))
            raise
