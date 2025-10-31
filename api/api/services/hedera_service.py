"""
Hedera network service for interacting with Hedera Mirror Node API
"""

import httpx
from typing import Dict, List, Optional, Any
import structlog
import asyncio
from concurrent.futures import ThreadPoolExecutor
from api.core.config import settings

logger = structlog.get_logger()

# Try to import Hedera SDK, but make it optional for MVP
try:
    from hedera import (
        Client, AccountId, PrivateKey, AccountCreateTransaction,
        Hbar, TransferTransaction, TransactionId, AccountBalanceQuery
    )
    HEDERA_AVAILABLE = True
except ImportError as e:
    logger.warning("Hedera SDK not available", error=str(e))
    HEDERA_AVAILABLE = False


class HederaService:
    """Service for interacting with Hedera network"""
    
    def __init__(self, environment: str = "testnet"):
        self.environment = environment
        self.mirror_url = (
            settings.HEDERA_TESTNET_URL if environment == "testnet"
            else settings.HEDERA_MAINNET_URL
        )
        self.client = None
        self.has_operator = False
        
        # Initialize Hedera client only if SDK is available
        if HEDERA_AVAILABLE:
            try:
                # Initialize Hedera client with operator credentials
                if environment == "testnet":
                    self.client = Client.forTestnet()
                    # Check if credentials are provided via environment variables
                    if settings.HEDERA_TESTNET_OPERATOR_ID and settings.HEDERA_TESTNET_OPERATOR_KEY:
                        try:
                            # Set operator for testnet using environment credentials
                            operator_id = AccountId.fromString(settings.HEDERA_TESTNET_OPERATOR_ID)
                            # Strip 0x prefix if present (common in exported keys)
                            operator_key_str = settings.HEDERA_TESTNET_OPERATOR_KEY
                            if operator_key_str.startswith('0x') or operator_key_str.startswith('0X'):
                                operator_key_str = operator_key_str[2:]
                            operator_key = PrivateKey.fromString(operator_key_str)
                            self.client.setOperator(operator_id, operator_key)
                            self.has_operator = True
                            logger.info("Hedera operator configured from environment variables")
                        except Exception as e:
                            logger.warning("Failed to set Hedera operator from environment, using mock mode", error=str(e))
                            self.has_operator = False
                    else:
                        logger.info("Hedera credentials not provided, using mock mode for transactions")
                        self.has_operator = False
                else:
                    self.client = Client.forMainnet()
                    # For mainnet, operator credentials should be provided via environment variables
                    # This is a placeholder - in production, use secure credential management
                    self.has_operator = False
            except Exception as e:
                logger.warning("Failed to initialize Hedera client, using mock mode", error=str(e))
                self.client = None
                self.has_operator = False
        else:
            logger.warning(
                "Hedera SDK not available. Install Java and hedera-sdk-py for full functionality. "
                "Read operations will use mirror node API. Write operations will use mock mode."
            )
            self.has_operator = False
    
    async def create_account(self, account_type: str = "user", metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new Hedera account"""
        try:
            # Check if we can create real accounts
            if not HEDERA_AVAILABLE or not self.client or not self.has_operator:
                # Use mock mode when SDK or operator is not available
                logger.info("Using mock mode for Hedera account creation", environment=self.environment)
                import hashlib
                import time
                
                # Generate deterministic but unique account ID for mock
                seed = f"{account_type}{str(metadata)}{time.time()}"
                account_hash = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % 1000000000
                mock_account_id = f"0.0.{account_hash}"
                
                return {
                    "account_id": mock_account_id,
                    "private_key": f"mock_hedera_private_{hashlib.sha256(seed.encode()).hexdigest()[:32]}",
                    "public_key": f"mock_hedera_public_{hashlib.sha256(seed.encode()).hexdigest()[:32]}",
                    "network": "hedera",
                    "environment": self.environment,
                    "account_type": account_type,
                    "metadata": metadata or {},
                    "note": "Mock account - install Hedera SDK and configure operator for real accounts"
                }
            
            # Generate new private key
            private_key = PrivateKey.generate()
            public_key = private_key.getPublicKey()
            
            # Create account transaction
            transaction = (
                AccountCreateTransaction()
                .setKey(public_key)
                .setInitialBalance(Hbar(1))  # Initial balance in HBAR (reduced for testing)
            )
            
            # Execute transaction with retry logic
            # Run blocking SDK calls in thread pool to avoid blocking async event loop
            try:
                loop = asyncio.get_event_loop()
                
                # Execute transaction in thread pool (blocking call)
                response = await loop.run_in_executor(
                    None,
                    lambda: transaction.execute(self.client)
                )
                
                # Get receipt in thread pool (blocking call)
                receipt = await loop.run_in_executor(
                    None,
                    lambda: response.getReceipt(self.client)
                )
                account_id_obj = receipt.accountId
                # Convert AccountId Java object to string using toString() method
                # AccountId is a Java object, call toString() method
                account_id = account_id_obj.toString()
                
            except Exception as network_error:
                logger.warning("Network error during account creation, falling back to mock", error=str(network_error))
                # Fall back to mock mode for network issues
                import hashlib
                import time
                seed = f"{account_type}{str(metadata)}{time.time()}"
                account_hash = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % 1000000000
                mock_account_id = f"0.0.{account_hash}"
                
                return {
                    "account_id": mock_account_id,
                    "private_key": f"mock_hedera_private_{hashlib.sha256(seed.encode()).hexdigest()[:32]}",
                    "public_key": f"mock_hedera_public_{hashlib.sha256(seed.encode()).hexdigest()[:32]}",
                    "network": "hedera",
                    "environment": self.environment,
                    "account_type": account_type,
                    "metadata": metadata or {},
                    "note": "Mock response due to network issues"
                }
            
            logger.info("Hedera account created", account_id=account_id, environment=self.environment)
            
            return {
                "account_id": account_id,
                "private_key": private_key.toString(),  # In production, this should be encrypted
                "public_key": public_key.toString(),
                "network": "hedera",
                "environment": self.environment,
                "account_type": account_type,
                "metadata": metadata or {}
            }
            
        except Exception as e:
            logger.error("Failed to create Hedera account", error=str(e))
            raise
    
    async def get_account_info(self, account_id: str) -> Dict[str, Any]:
        """Get account information from Hedera network"""
        try:
            # Get account info from mirror node (works without SDK)
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.mirror_url}/api/v1/accounts/{account_id}")
                
                if response.status_code == 404:
                    logger.warning("Hedera account not found", account_id=account_id)
                    return None
                
                response.raise_for_status()
                account_data = response.json()
            
            # Get balance from SDK if available, otherwise use mirror node data
            balance_hbars = "0"
            balance_tinybars = "0"
            
            if HEDERA_AVAILABLE and self.client:
                try:
                    # Parse account ID and get balance via SDK
                    account = AccountId.fromString(account_id)
                    balance_query = AccountBalanceQuery().setAccountId(account)
                    balance = balance_query.execute(self.client)
                    # Convert Hbar object to numeric value (in tinybars, then convert to HBAR)
                    balance_tinybars = int(balance.hbars.toTinybars())
                    balance_hbars_value = balance_tinybars / 100000000  # Convert tinybars to HBAR
                    balance_hbars = f"{balance_hbars_value:.8f}".rstrip('0').rstrip('.')  # Format with max 8 decimals
                    balance_tinybars = str(balance_tinybars)
                except Exception as e:
                    logger.warning("Failed to get balance via SDK, using mirror node data", error=str(e))
                    # Fall back to mirror node balance
                    balance_info = account_data.get("balance", {})
                    balance_value = balance_info.get("balance", 0)
                    if balance_value:
                        balance_hbars_value = balance_value / 100000000  # Convert tinybars to HBAR
                        balance_hbars = f"{balance_hbars_value:.8f}".rstrip('0').rstrip('.')
                    else:
                        balance_hbars = "0"
                    balance_tinybars = str(balance_value)
            else:
                # Use mirror node balance data
                balance_info = account_data.get("balance", {})
                balance_value = balance_info.get("balance", 0)
                if balance_value:
                    balance_hbars_value = balance_value / 100000000  # Convert tinybars to HBAR
                    balance_hbars = f"{balance_hbars_value:.8f}".rstrip('0').rstrip('.')
                else:
                    balance_hbars = "0"
                balance_tinybars = str(balance_value)
            
            return {
                "account_id": account_id,
                "balance": balance_hbars,
                "balance_tinybars": balance_tinybars,
                "account": account_data.get("account"),
                "balance_timestamp": account_data.get("balance", {}).get("timestamp"),
                "created_timestamp": account_data.get("created_timestamp"),
                "deleted": account_data.get("deleted", False),
                "key": account_data.get("key"),
                "memo": account_data.get("memo")
            }
            
        except Exception as e:
            logger.error("Failed to get Hedera account info", account_id=account_id, error=str(e))
            raise
    
    async def get_account_balances(self, account_id: str) -> List[Dict[str, Any]]:
        """Get account balances"""
        try:
            # Always try to get real account info from mirror node
            account_info = await self.get_account_info(account_id)
            
            if not account_info:
                # Account not found - return empty or mock for MVP
                if not HEDERA_AVAILABLE:
                    logger.info("Account not found, returning mock balance for MVP", account_id=account_id)
                    return [{
                        "asset_code": "HBAR",
                        "asset_issuer": None,
                        "balance": "0.00",
                        "balance_usd": "0.00",
                        "asset_type": "native",
                        "updated_at": None
                    }]
                return []
            
            # Get HBAR balance - ensure it's always a string, never an Hbar object
            balance_hbars_raw = account_info.get("balance", "0")
            
            # Convert to string if it's not already (handles any edge cases)
            if not isinstance(balance_hbars_raw, str):
                # If somehow we got an Hbar object or other type, convert it properly
                try:
                    if hasattr(balance_hbars_raw, 'toTinybars'):
                        # It's an Hbar object - convert to tinybars then to HBAR
                        balance_tinybars = int(balance_hbars_raw.toTinybars())
                        balance_hbars_value = balance_tinybars / 100000000
                        balance_hbars = f"{balance_hbars_value:.8f}".rstrip('0').rstrip('.')
                    else:
                        # Try to convert to float then string
                        balance_hbars = str(float(balance_hbars_raw))
                except (ValueError, TypeError, AttributeError):
                    balance_hbars = "0"
            else:
                balance_hbars = balance_hbars_raw
            
            # Ensure balance is a valid numeric string
            try:
                # Validate it's a valid number
                float(balance_hbars)
            except (ValueError, TypeError):
                balance_hbars = "0"
            
            # Calculate USD value (rough estimate: 1 HBAR ≈ $0.05)
            try:
                balance_usd = f"{float(balance_hbars) * 0.05:.2f}"
            except (ValueError, TypeError):
                balance_usd = "0.00"
            
            # For now, return HBAR balance
            # In the future, we can add token balances from mirror node API
            return [{
                "asset_code": "HBAR",
                "asset_issuer": None,
                "balance": balance_hbars,  # Now guaranteed to be a string
                "balance_usd": balance_usd,
                "asset_type": "native",
                "updated_at": account_info.get("balance_timestamp")
            }]
            
        except Exception as e:
            logger.error("Failed to get Hedera account balances", account_id=account_id, error=str(e))
            # Return empty list on error rather than raising
            return []
    
    async def create_payment_transaction(
        self,
        source_private_key: str,
        destination: str,
        amount: str,
        memo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a payment transaction (HBAR transfer)"""
        try:
            # Check if we can create real transactions
            if not HEDERA_AVAILABLE or not self.client:
                # Return mock transaction for MVP when SDK not available
                logger.info("Using mock mode for Hedera payment transaction", 
                          from_account=source_private_key[:20] if len(source_private_key) > 20 else source_private_key,
                          to_account=destination,
                          amount=amount)
                
                import hashlib
                import time
                import uuid
                tx_seed = f"{source_private_key}{destination}{amount}{time.time()}{uuid.uuid4()}"
                tx_hash = hashlib.sha256(tx_seed.encode()).hexdigest()[:32]
                
                return {
                    "transaction_hash": f"0.0.{int(tx_hash[:8], 16) % 1000000000}/{int(time.time())}",
                    "status": "pending",
                    "transaction_id": f"0.0.{int(tx_hash[:8], 16) % 1000000000}/{int(time.time())}",
                    "note": "Mock transaction - install Hedera SDK for real transactions"
                }
            
            # Check if source_private_key is actually a mock key
            if source_private_key.startswith("mock_hedera_private_"):
                logger.warning("Cannot execute transaction with mock private key")
                raise ValueError("Mock private keys cannot be used for real transactions. Create a real Hedera account first.")
            
            # Parse private key and account IDs
            try:
                private_key = PrivateKey.fromString(source_private_key)
                source_account = private_key.getPublicKey().getAccountId()
                destination_account = AccountId.fromString(destination)
            except Exception as e:
                logger.error("Failed to parse Hedera account IDs", error=str(e))
                raise ValueError(f"Invalid Hedera account or private key format: {str(e)}")
            
            # Create transfer transaction
            transaction = (
                TransferTransaction()
                .addHbarTransfer(source_account, Hbar.fromString(f"-{amount}"))
                .addHbarTransfer(destination_account, Hbar.fromString(amount))
            )
            
            # Add memo if provided
            if memo:
                transaction = transaction.setTransactionMemo(memo)
            
            # Sign the transaction
            transaction = transaction.freezeWith(self.client)
            transaction = transaction.sign(private_key)
            
            # Execute transaction
            response = transaction.execute(self.client)
            
            # Get receipt
            receipt = response.getReceipt(self.client)
            transaction_id = receipt.transactionId
            
            logger.info(
                "Hedera payment transaction created",
                transaction_id=str(transaction_id),
                from_account=str(source_account),
                to_account=destination,
                amount=amount
            )
            
            return {
                "transaction_hash": str(transaction_id),
                "status": "success",
                "transaction_id": str(transaction_id),
                "receipt": {
                    "status": str(receipt.status),
                    "account_id": str(receipt.accountId) if receipt.accountId else None,
                    "amount": str(receipt.amount) if receipt.amount else None
                }
            }
            
        except ValueError:
            raise  # Re-raise ValueError
        except Exception as e:
            logger.error("Failed to create Hedera payment transaction", error=str(e))
            raise
    
    async def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get transaction information from mirror node"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mirror_url}/api/v1/transactions/{transaction_id}")
                
                if response.status_code == 404:
                    logger.warning("Hedera transaction not found", transaction_id=transaction_id)
                    return None
                
                response.raise_for_status()
                transaction_data = response.json()
            
            return {
                "transaction_hash": transaction_id,
                "consensus_timestamp": transaction_data.get("consensus_timestamp"),
                "transaction_id": transaction_data.get("transaction_id"),
                "result": transaction_data.get("result"),
                "memo": transaction_data.get("memo"),
                "transaction_fee": transaction_data.get("transaction_fee"),
                "transfers": transaction_data.get("transfers", []),
                "operations": transaction_data.get("operations", [])
            }
            
        except Exception as e:
            logger.error("Failed to get Hedera transaction", transaction_id=transaction_id, error=str(e))
            raise
    
    async def get_account_transactions(
        self,
        account_id: str,
        limit: int = 100,
        order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get transactions for an account from mirror node"""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "account.id": account_id,
                    "limit": limit,
                    "order": order
                }
                response = await client.get(f"{self.mirror_url}/api/v1/transactions", params=params)
                response.raise_for_status()
                
                transactions_data = response.json()
            
            return [
                {
                    "transaction_hash": tx.get("transaction_id"),
                    "consensus_timestamp": tx.get("consensus_timestamp"),
                    "result": tx.get("result"),
                    "memo": tx.get("memo"),
                    "transaction_fee": tx.get("transaction_fee"),
                    "transfers": tx.get("transfers", []),
                    "operations": tx.get("operations", [])
                }
                for tx in transactions_data.get("transactions", [])
            ]
            
        except Exception as e:
            logger.error("Failed to get Hedera account transactions", account_id=account_id, error=str(e))
            raise
    
    async def stream_transactions(self, account_id: Optional[str] = None):
        """Stream transactions in real-time from mirror node"""
        try:
            async with httpx.AsyncClient() as client:
                params = {}
                if account_id:
                    params["account.id"] = account_id
                
                # Use server-sent events for streaming
                async with client.stream("GET", f"{self.mirror_url}/api/v1/transactions", params=params) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                import json
                                data = json.loads(line[6:])  # Remove "data: " prefix
                                yield data
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error("Failed to stream Hedera transactions", account_id=account_id, error=str(e))
            raise
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get Hedera network information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mirror_url}/api/v1/network/nodes")
                response.raise_for_status()
                nodes_data = response.json()
            
            return {
                "network": "hedera",
                "environment": self.environment,
                "mirror_url": self.mirror_url,
                "nodes": nodes_data.get("nodes", []),
                "current_environment": self.environment
            }
            
        except Exception as e:
            logger.error("Failed to get Hedera network info", error=str(e))
            raise
