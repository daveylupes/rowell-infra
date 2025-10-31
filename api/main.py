"""
Rowell Infra - Main FastAPI Application
Alchemy for Africa: Stellar + Hedera APIs & Analytics
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog

from api.core.config import settings
from api.core.database import init_db, get_db
from api.api.v1.api import api_router
from api.core.middleware import setup_middleware
from api.services.health_service import HealthService
from datetime import datetime, timezone

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Rowell Infra API", version=settings.VERSION)
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Rowell Infra API")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="Rowell Infra API",
        description="""
        # Rowell Infra API - Alchemy for Africa
        
        ## Overview
        The Rowell Infra API provides comprehensive access to blockchain infrastructure for African fintech applications, supporting both Stellar and Hedera networks.
        
        ## Features
        - **Account Management**: Create and manage blockchain accounts
        - **Transfer Operations**: Send and receive payments across networks
        - **Analytics & Reporting**: Comprehensive transaction analytics and insights
        - **KYC & Compliance**: Identity verification and compliance monitoring
        - **Multi-Network Support**: Stellar and Hedera blockchain integration
        
        ## Authentication
        Most endpoints require an API key. Include your API key in the request header:
        ```
        X-API-Key: your_api_key_here
        ```
        
        ## Rate Limiting
        - **Free Tier**: 100 requests per minute
        - **Pro Tier**: 1,000 requests per minute
        - **Enterprise**: Custom limits
        
        ## Error Handling
        All errors follow a consistent format with error codes and descriptive messages.
        
        ## Support
        - **Documentation**: [docs.rowellinfra.com](https://docs.rowellinfra.com)
        - **Support**: [support@rowellinfra.com](mailto:support@rowellinfra.com)
        - **Status**: [status.rowellinfra.com](https://status.rowellinfra.com)
        """,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        contact={
            "name": "Rowell Infra Support",
            "url": "https://docs.rowellinfra.com",
            "email": "support@rowellinfra.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        servers=[
            {
                "url": "https://api.rowellinfra.com",
                "description": "Production server"
            },
            {
                "url": "https://api-staging.rowellinfra.com", 
                "description": "Staging server"
            },
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            }
        ],
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    async def root():
        """Root endpoint with API information"""
        return {
            "name": "Rowell Infra API",
            "description": "Alchemy for Africa: Stellar + Hedera APIs & Analytics",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health",
            "networks": {
                "stellar": {
                    "testnet": settings.STELLAR_TESTNET_URL,
                    "mainnet": settings.STELLAR_MAINNET_URL
                },
                "hedera": {
                    "testnet": settings.HEDERA_TESTNET_URL,
                    "mainnet": settings.HEDERA_MAINNET_URL
                }
            }
        }
    
    @app.get("/health")
    async def health_check(db: AsyncSession = Depends(get_db)):
        """Comprehensive health check endpoint"""
        try:
            health_service = HealthService(db)
            health_status = await health_service.get_comprehensive_health()
            return health_status
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": settings.VERSION,
                "error": str(e)
            }
    
    @app.get("/healthz")
    async def liveness_check(db: AsyncSession = Depends(get_db)):
        """Kubernetes liveness probe endpoint (simple check)"""
        try:
            health_service = HealthService(db)
            return await health_service.get_liveness()
        except Exception:
            return {
                "status": "dead",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    @app.get("/ready")
    async def readiness_check(db: AsyncSession = Depends(get_db)):
        """Kubernetes readiness probe endpoint"""
        try:
            health_service = HealthService(db)
            return await health_service.get_readiness()
        except Exception:
            return {
                "status": "not_ready",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "reason": "Service unavailable"
            }
    
    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
