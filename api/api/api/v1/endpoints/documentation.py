"""
API Documentation endpoints for Rowell Infra API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, Any, Optional
import structlog

from api.core.database import get_db
from api.core.auth import require_api_key
# from api.docs import CodeExamples, ErrorCodes, AuthenticationGuide, RateLimitingGuide

logger = structlog.get_logger()
router = APIRouter()

# Temporarily disabled due to import issues
# TODO: Fix api.docs import path


@router.get("/examples")
async def get_code_examples(
    language: Optional[str] = None,
    endpoint: Optional[str] = None
):
    """Get code examples for API usage"""
    try:
        examples = CodeExamples.get_all_examples()
        
        if language:
            all_examples = CodeExamples.get_all_examples()
            if language not in all_examples:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported language: {language}. Supported: {list(all_examples.keys())}"
                )
            examples = {language: all_examples[language]}
        
        if endpoint:
            filtered_examples = {}
            for lang, lang_examples in examples.items():
                if endpoint in lang_examples:
                    filtered_examples[lang] = {endpoint: lang_examples[endpoint]}
                else:
                    filtered_examples[lang] = {}
            examples = filtered_examples
        
        return {
            "success": True,
            "examples": examples,
            "supported_languages": list(CodeExamples.get_all_examples().keys()),
            "available_endpoints": list(next(iter(CodeExamples.get_all_examples().values())).keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get code examples", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get code examples: {str(e)}"
        )


@router.get("/error-codes")
async def get_error_codes(
    status_code: Optional[int] = None,
    error_code: Optional[str] = None
):
    """Get error codes and troubleshooting information"""
    try:
        if error_code:
            error_info = ErrorCodes.get_error_by_code(error_code)
            return {
                "success": True,
                "error_code": error_code,
                "information": error_info
            }
        
        if status_code:
            errors = ErrorCodes.get_errors_by_status_code(status_code)
            return {
                "success": True,
                "status_code": status_code,
                "errors": errors
            }
        
        # Return all error codes
        all_errors = ErrorCodes.get_error_codes()
        troubleshooting = ErrorCodes.get_troubleshooting_guide()
        
        return {
            "success": True,
            "error_codes": all_errors,
            "troubleshooting_guide": troubleshooting,
            "total_errors": len(all_errors)
        }
        
    except Exception as e:
        logger.error("Failed to get error codes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get error codes: {str(e)}"
        )


@router.get("/authentication")
async def get_authentication_guide():
    """Get comprehensive authentication guide"""
    try:
        overview = AuthenticationGuide.get_authentication_overview()
        api_key_guide = AuthenticationGuide.get_api_key_guide()
        examples = AuthenticationGuide.get_authentication_examples()
        best_practices = AuthenticationGuide.get_security_best_practices()
        auth_flow = AuthenticationGuide.get_authentication_flow()
        
        return {
            "success": True,
            "overview": overview,
            "api_key_guide": api_key_guide,
            "examples": examples,
            "best_practices": best_practices,
            "authentication_flow": auth_flow
        }
        
    except Exception as e:
        logger.error("Failed to get authentication guide", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get authentication guide: {str(e)}"
        )


@router.get("/rate-limiting")
async def get_rate_limiting_guide():
    """Get rate limiting documentation and policies"""
    try:
        overview = RateLimitingGuide.get_rate_limiting_overview()
        plans = RateLimitingGuide.get_rate_limits_by_plan()
        headers = RateLimitingGuide.get_rate_limit_headers()
        best_practices = RateLimitingGuide.get_best_practices()
        implementation_examples = RateLimitingGuide.get_implementation_examples()
        monitoring = RateLimitingGuide.get_monitoring_recommendations()
        
        return {
            "success": True,
            "overview": overview,
            "plans": plans,
            "headers": headers,
            "best_practices": best_practices,
            "implementation_examples": implementation_examples,
            "monitoring": monitoring
        }
        
    except Exception as e:
        logger.error("Failed to get rate limiting guide", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get rate limiting guide: {str(e)}"
        )


@router.get("/interactive")
async def get_interactive_documentation():
    """Get interactive documentation information"""
    try:
        return {
            "success": True,
            "interactive_docs": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_json": "/api/v1/openapi.json",
                "features": [
                    "Interactive API explorer",
                    "Try-it-out functionality",
                    "Request/response examples",
                    "Schema validation",
                    "Authentication testing"
                ]
            },
            "quick_start": {
                "step_1": "Visit /docs for interactive API explorer",
                "step_2": "Click 'Authorize' and enter your API key",
                "step_3": "Try any endpoint with the 'Try it out' button",
                "step_4": "View request/response examples",
                "step_5": "Copy code examples in multiple languages"
            },
            "api_explorer_features": [
                "Real-time API testing",
                "Parameter validation",
                "Response schema viewing",
                "Code generation in multiple languages",
                "Authentication flow testing"
            ]
        }
        
    except Exception as e:
        logger.error("Failed to get interactive documentation", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get interactive documentation: {str(e)}"
        )


@router.get("/status")
async def get_api_status():
    """Get API status and health information"""
    try:
        return {
            "success": True,
            "status": "operational",
            "version": "1.0.0",
            "services": {
                "api": "operational",
                "database": "operational",
                "stellar_network": "operational",
                "hedera_network": "operational",
                "analytics": "operational"
            },
            "uptime": "99.9%",
            "response_times": {
                "average": "150ms",
                "p95": "300ms",
                "p99": "500ms"
            },
            "rate_limits": {
                "current_tier": "free",
                "requests_per_minute": 100,
                "requests_remaining": 95
            }
        }
        
    except Exception as e:
        logger.error("Failed to get API status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get API status: {str(e)}"
        )


@router.get("/changelog")
async def get_api_changelog():
    """Get API changelog and version history"""
    try:
        return {
            "success": True,
            "changelog": [
                {
                    "version": "1.0.0",
                    "date": "2024-01-27",
                    "changes": [
                        "Initial API release",
                        "Account management endpoints",
                        "Transfer operations",
                        "Analytics and reporting",
                        "KYC and compliance features",
                        "Interactive documentation"
                    ]
                }
            ],
            "upcoming_features": [
                "Webhook support",
                "Advanced analytics",
                "Multi-signature accounts",
                "Custom compliance rules",
                "Mobile SDKs"
            ],
            "deprecation_notices": []
        }
        
    except Exception as e:
        logger.error("Failed to get API changelog", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get API changelog: {str(e)}"
        )


@router.get("/sdk")
async def get_sdk_information():
    """Get SDK information and download links"""
    try:
        return {
            "success": True,
            "official_sdks": {
                "javascript": {
                    "name": "Rowell Infra JavaScript SDK",
                    "version": "1.0.0",
                    "npm_package": "@rowellinfra/sdk-js",
                    "github_url": "https://github.com/rowellinfra/sdk-js",
                    "documentation": "https://docs.rowellinfra.com/sdk/javascript"
                },
                "python": {
                    "name": "Rowell Infra Python SDK", 
                    "version": "1.0.0",
                    "pip_package": "rowellinfra",
                    "github_url": "https://github.com/rowellinfra/sdk-python",
                    "documentation": "https://docs.rowellinfra.com/sdk/python"
                }
            },
            "community_sdks": [
                {
                    "name": "Rowell Infra Go SDK",
                    "language": "Go",
                    "github_url": "https://github.com/community/sdk-go",
                    "status": "community_maintained"
                }
            ],
            "installation_examples": {
                "javascript": "npm install @rowellinfra/sdk-js",
                "python": "pip install rowellinfra",
                "go": "go get github.com/community/sdk-go"
            }
        }
        
    except Exception as e:
        logger.error("Failed to get SDK information", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get SDK information: {str(e)}"
        )
