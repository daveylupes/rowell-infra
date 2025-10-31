"""
Custom middleware for Rowell Infra API
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import structlog
from api.core.config import settings

logger = structlog.get_logger()


async def logging_middleware(request: Request, call_next):
    """Log all requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=round(process_time, 4),
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


async def rate_limit_middleware(request: Request, call_next):
    """Basic rate limiting middleware"""
    # TODO: Implement proper rate limiting with Redis
    # For now, just pass through
    response = await call_next(request)
    return response


def setup_middleware(app: FastAPI):
    """Setup all middleware for the application"""
    
    # CORS middleware - in debug mode, allow all origins for Swagger UI
    cors_origins = settings.BACKEND_CORS_ORIGINS
    if settings.DEBUG:
        # In debug mode, allow all origins (including Swagger UI self-requests)
        cors_origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.DEBUG else ["rowell-infra.com", "*.rowell-infra.com"]
    )
    
    # Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Custom middleware
    app.middleware("http")(logging_middleware)
    app.middleware("http")(rate_limit_middleware)
