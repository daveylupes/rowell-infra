"""
Secure Key Storage Service
Handles secure storage and retrieval of private keys/secrets
"""

import secrets
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models.account import Account
import structlog
from cryptography.fernet import Fernet
from api.core.config import settings

logger = structlog.get_logger()

# In-memory key storage for one-time tokens (in production, use Redis)
_key_storage: Dict[str, Dict[str, Any]] = {}


class KeyStorageService:
    """Service for secure key storage and retrieval"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # Use encryption key from settings (should be in environment variables)
        try:
            from api.core.config import settings
            if settings.KEY_ENCRYPTION_KEY:
                self.cipher = Fernet(settings.KEY_ENCRYPTION_KEY.encode())
            else:
                # Generate a key for development (NOT for production!)
                logger.warning("KEY_ENCRYPTION_KEY not set in environment. Using generated key (NOT SECURE FOR PRODUCTION)")
                self.cipher = Fernet(Fernet.generate_key())
        except ImportError:
            # Fallback if cryptography not available
            self.cipher = None
            logger.warning("Fernet encryption not available, using base64 encoding")
        except Exception as e:
            logger.warning(f"Failed to initialize cipher, using base64 encoding: {str(e)}")
            self.cipher = None
    
    def _generate_token(self) -> str:
        """Generate a secure one-time token"""
        return secrets.token_urlsafe(32)
    
    def _encrypt_key(self, key: str) -> str:
        """Encrypt private key before storage"""
        if self.cipher:
            return self.cipher.encrypt(key.encode()).decode()
        # Fallback: base64 encoding (NOT secure, but better than plaintext)
        import base64
        return base64.b64encode(key.encode()).decode()
    
    def _decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt private key for retrieval"""
        if self.cipher:
            return self.cipher.decrypt(encrypted_key.encode()).decode()
        # Fallback
        import base64
        return base64.b64decode(encrypted_key.encode()).decode()
    
    async def store_key(
        self,
        account_id: str,
        private_key: str,
        network: str,
        expires_in_minutes: int = 30
    ) -> str:
        """
        Store private key securely and return one-time token
        
        Args:
            account_id: The blockchain account ID
            private_key: The private/secret key to store
            network: Network (stellar/hedera)
            expires_in_minutes: Token expiration time
            
        Returns:
            One-time token for key retrieval
        """
        try:
            token = self._generate_token()
            encrypted_key = self._encrypt_key(private_key)
            expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
            
            # Store in memory (in production, use Redis with TTL)
            _key_storage[token] = {
                "account_id": account_id,
                "encrypted_key": encrypted_key,
                "network": network,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": expires_at.isoformat(),
                "retrieved": False
            }
            
            logger.info(
                "Private key stored securely",
                account_id=account_id,
                network=network,
                expires_at=expires_at.isoformat()
            )
            
            return token
            
        except Exception as e:
            logger.error("Failed to store private key", error=str(e))
            raise
    
    async def retrieve_key(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve private key using one-time token
        
        Args:
            token: One-time token from store_key
            
        Returns:
            Dict with account_id and private_key, or None if invalid/expired
        """
        try:
            if token not in _key_storage:
                logger.warning("Invalid key retrieval token")
                return None
            
            key_data = _key_storage[token]
            
            # Check expiration
            expires_at = datetime.fromisoformat(key_data["expires_at"])
            if datetime.utcnow() > expires_at:
                logger.warning("Key retrieval token expired", token=token[:8])
                del _key_storage[token]
                return None
            
            # Check if already retrieved (one-time use)
            if key_data.get("retrieved", False):
                logger.warning("Key retrieval token already used", token=token[:8])
                del _key_storage[token]
                return None
            
            # Mark as retrieved
            key_data["retrieved"] = True
            
            # Decrypt and return
            private_key = self._decrypt_key(key_data["encrypted_key"])
            
            logger.info("Private key retrieved", account_id=key_data["account_id"])
            
            return {
                "account_id": key_data["account_id"],
                "private_key": private_key,
                "network": key_data["network"]
            }
            
        except Exception as e:
            logger.error("Failed to retrieve private key", error=str(e))
            return None
    
    async def revoke_token(self, token: str) -> bool:
        """Revoke a key retrieval token"""
        try:
            if token in _key_storage:
                del _key_storage[token]
                logger.info("Key token revoked", token=token[:8])
                return True
            return False
        except Exception as e:
            logger.error("Failed to revoke token", error=str(e))
            return False
    
    async def cleanup_expired_tokens(self):
        """Clean up expired tokens from storage"""
        try:
            current_time = datetime.utcnow()
            expired_tokens = [
                token for token, data in _key_storage.items()
                if datetime.fromisoformat(data["expires_at"]) < current_time
            ]
            
            for token in expired_tokens:
                del _key_storage[token]
            
            if expired_tokens:
                logger.info(f"Cleaned up {len(expired_tokens)} expired tokens")
                
        except Exception as e:
            logger.error("Failed to cleanup expired tokens", error=str(e))

