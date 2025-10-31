"""
Health Check Service
Comprehensive health checking for all system components
"""

import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from api.core.config import settings
import structlog

logger = structlog.get_logger()


class HealthService:
    """Service for checking system health"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and response time"""
        start_time = time.time()
        try:
            result = await self.db.execute(text("SELECT 1"))
            result.fetchone()
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "message": "Database connection successful"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "error": str(e),
                "message": "Database connection failed"
            }
    
    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            import redis.asyncio as redis
            start_time = time.time()
            
            # Try to connect to Redis
            redis_client = redis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            await redis_client.ping()
            await redis_client.aclose()
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "message": "Redis connection successful"
            }
        except ImportError:
            return {
                "status": "degraded",
                "response_time_ms": None,
                "message": "Redis client not installed"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "error": str(e),
                "message": "Redis connection failed"
            }
    
    async def check_stellar(self, environment: str = "testnet") -> Dict[str, Any]:
        """Check Stellar network connectivity"""
        start_time = time.time()
        try:
            url = (
                settings.STELLAR_TESTNET_URL if environment == "testnet"
                else settings.STELLAR_MAINNET_URL
            )
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{url}/accounts/GDZ55")
                
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 404 or response.status_code == 200:
                    # 404 is OK - means network is responding
                    return {
                        "status": "healthy",
                        "response_time_ms": round(response_time, 2),
                        "network": environment,
                        "url": url,
                        "message": "Stellar network accessible"
                    }
                else:
                    return {
                        "status": "degraded",
                        "response_time_ms": round(response_time, 2),
                        "network": environment,
                        "url": url,
                        "error": f"HTTP {response.status_code}",
                        "message": "Stellar network returned unexpected status"
                    }
                    
        except httpx.TimeoutException:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "network": environment,
                "error": "Timeout",
                "message": "Stellar network timeout"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "network": environment,
                "error": str(e),
                "message": "Stellar network unreachable"
            }
    
    async def check_hedera(self, environment: str = "testnet") -> Dict[str, Any]:
        """Check Hedera network connectivity"""
        start_time = time.time()
        try:
            url = (
                settings.HEDERA_TESTNET_URL if environment == "testnet"
                else settings.HEDERA_MAINNET_URL
            )
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Check mirror node API
                response = await client.get(f"{url}/api/v1/accounts/0.0.2")
                
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code in [200, 404]:
                    # Either response means network is accessible
                    return {
                        "status": "healthy",
                        "response_time_ms": round(response_time, 2),
                        "network": environment,
                        "url": url,
                        "message": "Hedera network accessible"
                    }
                else:
                    return {
                        "status": "degraded",
                        "response_time_ms": round(response_time, 2),
                        "network": environment,
                        "url": url,
                        "error": f"HTTP {response.status_code}",
                        "message": "Hedera network returned unexpected status"
                    }
                    
        except httpx.TimeoutException:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "network": environment,
                "error": "Timeout",
                "message": "Hedera network timeout"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "network": environment,
                "error": str(e),
                "message": "Hedera network unreachable"
            }
    
    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health check for all components"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Run all health checks in parallel
        db_check, redis_check, stellar_testnet, stellar_mainnet, hedera_testnet, hedera_mainnet = await asyncio.gather(
            self.check_database(),
            self.check_redis(),
            self.check_stellar("testnet"),
            self.check_stellar("mainnet"),
            self.check_hedera("testnet"),
            self.check_hedera("mainnet"),
            return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(db_check, Exception):
            db_check = {"status": "unhealthy", "error": str(db_check)}
        if isinstance(redis_check, Exception):
            redis_check = {"status": "unhealthy", "error": str(redis_check)}
        if isinstance(stellar_testnet, Exception):
            stellar_testnet = {"status": "unhealthy", "error": str(stellar_testnet)}
        if isinstance(stellar_mainnet, Exception):
            stellar_mainnet = {"status": "unhealthy", "error": str(stellar_mainnet)}
        if isinstance(hedera_testnet, Exception):
            hedera_testnet = {"status": "unhealthy", "error": str(hedera_testnet)}
        if isinstance(hedera_mainnet, Exception):
            hedera_mainnet = {"status": "unhealthy", "error": str(hedera_mainnet)}
        
        # Determine overall status
        all_statuses = [
            db_check.get("status"),
            redis_check.get("status"),
            stellar_testnet.get("status"),
            stellar_mainnet.get("status"),
            hedera_testnet.get("status"),
            hedera_mainnet.get("status"),
        ]
        
        if "unhealthy" in all_statuses:
            overall_status = "unhealthy"
        elif "degraded" in all_statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"
        
        return {
            "status": overall_status,
            "timestamp": timestamp,
            "version": settings.VERSION,
            "components": {
                "database": db_check,
                "redis": redis_check,
                "stellar": {
                    "testnet": stellar_testnet,
                    "mainnet": stellar_mainnet,
                },
                "hedera": {
                    "testnet": hedera_testnet,
                    "mainnet": hedera_mainnet,
                },
            },
            "summary": {
                "total_components": 6,
                "healthy": sum(1 for s in all_statuses if s == "healthy"),
                "degraded": sum(1 for s in all_statuses if s == "degraded"),
                "unhealthy": sum(1 for s in all_statuses if s == "unhealthy"),
            }
        }
    
    async def get_liveness(self) -> Dict[str, Any]:
        """Simple liveness check (for Kubernetes /healthz)"""
        return {
            "status": "alive",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_readiness(self) -> Dict[str, Any]:
        """Readiness check - requires critical components to be healthy"""
        db_check = await self.check_database()
        
        if db_check.get("status") != "healthy":
            return {
                "status": "not_ready",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "reason": "Database unavailable"
            }
        
        return {
            "status": "ready",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

