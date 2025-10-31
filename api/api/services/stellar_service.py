"""
Stellar network service for interacting with Stellar Horizon API
"""

import httpx
from typing import Dict, List, Optional, Any
from stellar_sdk import Server, Keypair, Network, TransactionBuilder, Asset
from stellar_sdk.exceptions import NotFoundError, BadRequestError
import structlog
from api.core.config import settings

logger = structlog.get_logger()


class StellarService:
    """Service for interacting with Stellar network"""
    
    def __init__(self, environment: str = "testnet"):
        self.environment = environment
        self.network_passphrase = (
            settings.STELLAR_TESTNET_PASSPHRASE if environment == "testnet"
            else settings.STELLAR_MAINNET_PASSPHRASE
        )
        self.horizon_url = (
            settings.STELLAR_TESTNET_URL if environment == "testnet"
            else settings.STELLAR_MAINNET_URL
        )
        self.server = Server(self.horizon_url)
        # Set network passphrase for transactions
        try:
            if environment == "testnet":
                Network.use_testnet_network()
            else:
                Network.use_public_network()
        except AttributeError:
            # For newer versions of stellar-sdk, use different approach
            pass
    
    async def create_account(self, account_type: str = "user", metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new Stellar account"""
        try:
            # Generate new keypair
            keypair = Keypair.random()
            account_id = keypair.public_key
            secret_key = keypair.secret
            
            # For testnet, we can fund the account with friendbot
            if self.environment == "testnet":
                await self._fund_testnet_account(account_id)
            
            logger.info("Stellar account created", account_id=account_id, environment=self.environment)
            
            return {
                "account_id": account_id,
                "secret_key": secret_key,  # In production, this should be encrypted
                "network": "stellar",
                "environment": self.environment,
                "account_type": account_type,
                "metadata": metadata or {}
            }
            
        except Exception as e:
            logger.error("Failed to create Stellar account", error=str(e))
            raise
    
    async def _fund_testnet_account(self, account_id: str) -> None:
        """Fund testnet account using friendbot"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://friendbot.stellar.org",
                    params={"addr": account_id}
                )
                response.raise_for_status()
                logger.info("Testnet account funded", account_id=account_id)
        except Exception as e:
            logger.warning("Failed to fund testnet account", account_id=account_id, error=str(e))
    
    async def get_account_info(self, account_id: str) -> Dict[str, Any]:
        """Get account information from Stellar network"""
        try:
            account = self.server.accounts().account_id(account_id).call()
            
            # Parse account data
            balances = []
            for balance in account.get("balances", []):
                balances.append({
                    "asset_code": balance.get("asset_code", "XLM"),
                    "asset_issuer": balance.get("asset_issuer"),
                    "balance": balance.get("balance"),
                    "asset_type": balance.get("asset_type")
                })
            
            return {
                "account_id": account_id,
                "sequence": account.get("sequence"),
                "balances": balances,
                "flags": account.get("flags"),
                "signers": account.get("signers"),
                "data": account.get("data", {}),
                "created_at": account.get("created_at")
            }
            
        except NotFoundError:
            logger.warning("Stellar account not found", account_id=account_id)
            return None
        except Exception as e:
            # Log error but don't raise - return None to indicate account not found/invalid
            # This allows the balance endpoint to return empty list instead of 500 error
            error_msg = str(e)
            if "400" in error_msg or "Bad Request" in error_msg:
                logger.warning("Invalid Stellar account ID or account doesn't exist", account_id=account_id, error=error_msg)
            else:
                logger.error("Failed to get Stellar account info", account_id=account_id, error=error_msg)
            return None
    
    async def get_account_balances(self, account_id: str) -> List[Dict[str, Any]]:
        """Get account balances"""
        account_info = await self.get_account_info(account_id)
        if not account_info:
            return []
        
        return account_info.get("balances", [])
    
    async def create_payment_transaction(
        self,
        source_secret: str,
        destination: str,
        asset_code: str,
        amount: str,
        asset_issuer: Optional[str] = None,
        memo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a payment transaction"""
        try:
            source_keypair = Keypair.from_secret(source_secret)
            source_account = self.server.load_account(source_keypair.public_key)
            
            # Create asset
            if asset_code == "XLM":
                asset = Asset.native()
            else:
                if not asset_issuer:
                    raise ValueError("Asset issuer required for non-native assets")
                asset = Asset(asset_code, asset_issuer)
            
            # Build transaction
            builder = TransactionBuilder(
                source_account=source_account,
                network_passphrase=self.network_passphrase,
                base_fee=100  # Base fee in stroops
            )
            
            if memo:
                builder.add_text_memo(memo)
            
            builder.append_payment_op(
                destination=destination,
                asset=asset,
                amount=amount
            )
            
            builder.set_timeout(300)  # 5 minutes
            transaction = builder.build()
            
            # Sign transaction
            transaction.sign(source_keypair)
            
            # Submit transaction
            response = self.server.submit_transaction(transaction)
            
            logger.info(
                "Stellar payment transaction created",
                transaction_hash=response.get("hash"),
                from_account=source_keypair.public_key,
                to_account=destination,
                amount=amount,
                asset_code=asset_code
            )
            
            return {
                "transaction_hash": response.get("hash"),
                "status": "success" if response.get("successful") else "failed",
                "ledger": response.get("ledger"),
                "created_at": response.get("created_at"),
                "fee_charged": response.get("fee_charged"),
                "result_xdr": response.get("result_xdr")
            }
            
        except Exception as e:
            logger.error("Failed to create Stellar payment transaction", error=str(e))
            raise
    
    async def get_transaction(self, transaction_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction information"""
        try:
            transaction = self.server.transactions().transaction(transaction_hash).call()
            
            return {
                "transaction_hash": transaction.get("hash"),
                "ledger": transaction.get("ledger"),
                "created_at": transaction.get("created_at"),
                "source_account": transaction.get("source_account"),
                "fee_charged": transaction.get("fee_charged"),
                "successful": transaction.get("successful"),
                "operations": transaction.get("operations", []),
                "memo": transaction.get("memo"),
                "memo_type": transaction.get("memo_type")
            }
            
        except NotFoundError:
            logger.warning("Stellar transaction not found", transaction_hash=transaction_hash)
            return None
        except Exception as e:
            logger.error("Failed to get Stellar transaction", transaction_hash=transaction_hash, error=str(e))
            raise
    
    async def get_account_transactions(
        self,
        account_id: str,
        limit: int = 100,
        order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get transactions for an account"""
        try:
            transactions = (
                self.server.transactions()
                .for_account(account_id)
                .limit(limit)
                .order(order)
                .call()
            )
            
            return [
                {
                    "transaction_hash": tx.get("hash"),
                    "ledger": tx.get("ledger"),
                    "created_at": tx.get("created_at"),
                    "source_account": tx.get("source_account"),
                    "fee_charged": tx.get("fee_charged"),
                    "successful": tx.get("successful"),
                    "operations": tx.get("operations", []),
                    "memo": tx.get("memo")
                }
                for tx in transactions.get("_embedded", {}).get("records", [])
            ]
            
        except Exception as e:
            logger.error("Failed to get Stellar account transactions", account_id=account_id, error=str(e))
            raise
    
    async def stream_transactions(self, account_id: Optional[str] = None):
        """Stream transactions in real-time"""
        try:
            if account_id:
                # Stream transactions for specific account
                for response in self.server.transactions().for_account(account_id).cursor("now").stream():
                    yield response
            else:
                # Stream all transactions
                for response in self.server.transactions().cursor("now").stream():
                    yield response
                    
        except Exception as e:
            logger.error("Failed to stream Stellar transactions", account_id=account_id, error=str(e))
            raise
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get Stellar network information"""
        try:
            # Get network info from horizon
            root = self.server.root().call()
            
            return {
                "network": "stellar",
                "environment": self.environment,
                "horizon_version": root.get("horizon_version"),
                "core_version": root.get("core_version"),
                "network_passphrase": self.network_passphrase,
                "current_ledger": root.get("core_latest_ledger"),
                "current_ledger_time": root.get("core_latest_ledger_close_time")
            }
            
        except Exception as e:
            logger.error("Failed to get Stellar network info", error=str(e))
            raise
