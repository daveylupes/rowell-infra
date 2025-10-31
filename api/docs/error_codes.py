"""
Error codes and troubleshooting guide for Rowell Infra API
"""

from typing import Dict, List, Any
from enum import Enum


class ErrorCode(Enum):
    """Standard error codes for the API"""
    
    # Authentication & Authorization
    AUTH_REQUIRED = "AUTH_REQUIRED"
    AUTH_INVALID = "AUTH_INVALID"
    AUTH_EXPIRED = "AUTH_EXPIRED"
    AUTH_INSUFFICIENT_PERMISSIONS = "AUTH_INSUFFICIENT_PERMISSIONS"
    
    # Validation Errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_FORMAT = "INVALID_FORMAT"
    
    # Account Errors
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"
    ACCOUNT_ALREADY_EXISTS = "ACCOUNT_ALREADY_EXISTS"
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    
    # Transfer Errors
    TRANSFER_NOT_FOUND = "TRANSFER_NOT_FOUND"
    TRANSFER_FAILED = "TRANSFER_FAILED"
    TRANSFER_INVALID_AMOUNT = "TRANSFER_INVALID_AMOUNT"
    TRANSFER_INVALID_ASSET = "TRANSFER_INVALID_ASSET"
    TRANSFER_BLOCKED = "TRANSFER_BLOCKED"
    
    # Compliance Errors
    COMPLIANCE_CHECK_FAILED = "COMPLIANCE_CHECK_FAILED"
    KYC_REQUIRED = "KYC_REQUIRED"
    KYC_VERIFICATION_FAILED = "KYC_VERIFICATION_FAILED"
    SANCTIONS_HIT = "SANCTIONS_HIT"
    
    # Rate Limiting
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # Network Errors
    NETWORK_ERROR = "NETWORK_ERROR"
    BLOCKCHAIN_UNAVAILABLE = "BLOCKCHAIN_UNAVAILABLE"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    
    # Server Errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"


class ErrorCodes:
    """Comprehensive error code documentation and troubleshooting"""
    
    @staticmethod
    def get_error_codes() -> Dict[str, Dict[str, Any]]:
        """Get all error codes with descriptions and troubleshooting"""
        return {
            ErrorCode.AUTH_REQUIRED.value: {
                "http_status": 401,
                "title": "Authentication Required",
                "description": "The request requires authentication. Please provide a valid API key.",
                "solution": "Include your API key in the request header: X-API-Key: your_api_key_here",
                "example": {
                    "error": "Authentication required",
                    "code": "AUTH_REQUIRED",
                    "details": "No API key provided in request"
                }
            },
            ErrorCode.AUTH_INVALID.value: {
                "http_status": 401,
                "title": "Invalid Authentication",
                "description": "The provided API key is invalid or malformed.",
                "solution": "Verify your API key is correct and properly formatted",
                "example": {
                    "error": "Invalid authentication",
                    "code": "AUTH_INVALID", 
                    "details": "API key format is invalid"
                }
            },
            ErrorCode.AUTH_EXPIRED.value: {
                "http_status": 401,
                "title": "Authentication Expired",
                "description": "The API key has expired and needs to be renewed.",
                "solution": "Generate a new API key from your dashboard",
                "example": {
                    "error": "Authentication expired",
                    "code": "AUTH_EXPIRED",
                    "details": "API key expired on 2024-01-01T00:00:00Z"
                }
            },
            ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS.value: {
                "http_status": 403,
                "title": "Insufficient Permissions",
                "description": "Your API key doesn't have permission to perform this action.",
                "solution": "Contact support to upgrade your API key permissions",
                "example": {
                    "error": "Insufficient permissions",
                    "code": "AUTH_INSUFFICIENT_PERMISSIONS",
                    "details": "Required scope: transfers:write"
                }
            },
            ErrorCode.VALIDATION_ERROR.value: {
                "http_status": 400,
                "title": "Validation Error",
                "description": "The request data failed validation checks.",
                "solution": "Check the request format and required fields",
                "example": {
                    "error": "Validation failed",
                    "code": "VALIDATION_ERROR",
                    "details": {
                        "field": "amount",
                        "message": "Amount must be a positive number"
                    }
                }
            },
            ErrorCode.INVALID_PARAMETER.value: {
                "http_status": 400,
                "title": "Invalid Parameter",
                "description": "One or more request parameters are invalid.",
                "solution": "Verify parameter values and formats",
                "example": {
                    "error": "Invalid parameter",
                    "code": "INVALID_PARAMETER",
                    "details": {
                        "parameter": "network",
                        "value": "bitcoin",
                        "allowed_values": ["stellar", "hedera"]
                    }
                }
            },
            ErrorCode.MISSING_REQUIRED_FIELD.value: {
                "http_status": 400,
                "title": "Missing Required Field",
                "description": "A required field is missing from the request.",
                "solution": "Include all required fields in your request",
                "example": {
                    "error": "Missing required field",
                    "code": "MISSING_REQUIRED_FIELD",
                    "details": {
                        "field": "to_account",
                        "message": "Field is required"
                    }
                }
            },
            ErrorCode.INVALID_FORMAT.value: {
                "http_status": 400,
                "title": "Invalid Format",
                "description": "A field has an invalid format or type.",
                "solution": "Check the field format requirements in the API documentation",
                "example": {
                    "error": "Invalid format",
                    "code": "INVALID_FORMAT",
                    "details": {
                        "field": "date_of_birth",
                        "expected_format": "YYYY-MM-DD",
                        "provided_value": "01/01/1990"
                    }
                }
            },
            ErrorCode.ACCOUNT_NOT_FOUND.value: {
                "http_status": 404,
                "title": "Account Not Found",
                "description": "The specified account does not exist.",
                "solution": "Verify the account ID is correct and the account exists",
                "example": {
                    "error": "Account not found",
                    "code": "ACCOUNT_NOT_FOUND",
                    "details": "Account ID: acc_123456 not found"
                }
            },
            ErrorCode.ACCOUNT_INACTIVE.value: {
                "http_status": 400,
                "title": "Account Inactive",
                "description": "The account is inactive and cannot perform operations.",
                "solution": "Contact support to activate the account",
                "example": {
                    "error": "Account inactive",
                    "code": "ACCOUNT_INACTIVE",
                    "details": "Account status: suspended"
                }
            },
            ErrorCode.ACCOUNT_ALREADY_EXISTS.value: {
                "http_status": 409,
                "title": "Account Already Exists",
                "description": "An account with the same identifier already exists.",
                "solution": "Use a different identifier or retrieve the existing account",
                "example": {
                    "error": "Account already exists",
                    "code": "ACCOUNT_ALREADY_EXISTS",
                    "details": "Account with identifier already registered"
                }
            },
            ErrorCode.INSUFFICIENT_BALANCE.value: {
                "http_status": 400,
                "title": "Insufficient Balance",
                "description": "The account doesn't have sufficient balance for the operation.",
                "solution": "Check account balance and fund if necessary",
                "example": {
                    "error": "Insufficient balance",
                    "code": "INSUFFICIENT_BALANCE",
                    "details": {
                        "required": "100.00 USDC",
                        "available": "50.00 USDC"
                    }
                }
            },
            ErrorCode.TRANSFER_NOT_FOUND.value: {
                "http_status": 404,
                "title": "Transfer Not Found",
                "description": "The specified transfer does not exist.",
                "solution": "Verify the transfer ID is correct",
                "example": {
                    "error": "Transfer not found",
                    "code": "TRANSFER_NOT_FOUND",
                    "details": "Transfer ID: tx_123456 not found"
                }
            },
            ErrorCode.TRANSFER_FAILED.value: {
                "http_status": 400,
                "title": "Transfer Failed",
                "description": "The transfer operation failed on the blockchain.",
                "solution": "Check transfer parameters and try again",
                "example": {
                    "error": "Transfer failed",
                    "code": "TRANSFER_FAILED",
                    "details": "Blockchain transaction failed: insufficient balance"
                }
            },
            ErrorCode.TRANSFER_INVALID_AMOUNT.value: {
                "http_status": 400,
                "title": "Invalid Transfer Amount",
                "description": "The transfer amount is invalid.",
                "solution": "Ensure amount is positive and within allowed limits",
                "example": {
                    "error": "Invalid transfer amount",
                    "code": "TRANSFER_INVALID_AMOUNT",
                    "details": {
                        "amount": "-100.00",
                        "message": "Amount must be positive"
                    }
                }
            },
            ErrorCode.TRANSFER_INVALID_ASSET.value: {
                "http_status": 400,
                "title": "Invalid Transfer Asset",
                "description": "The specified asset is not supported or invalid.",
                "solution": "Check supported assets for the network",
                "example": {
                    "error": "Invalid transfer asset",
                    "code": "TRANSFER_INVALID_ASSET",
                    "details": {
                        "asset": "BTC",
                        "supported_assets": ["USDC", "XLM", "HBAR"]
                    }
                }
            },
            ErrorCode.TRANSFER_BLOCKED.value: {
                "http_status": 403,
                "title": "Transfer Blocked",
                "description": "The transfer is blocked due to compliance or risk rules.",
                "solution": "Contact compliance team for review",
                "example": {
                    "error": "Transfer blocked",
                    "code": "TRANSFER_BLOCKED",
                    "details": "Transfer flagged for compliance review"
                }
            },
            ErrorCode.COMPLIANCE_CHECK_FAILED.value: {
                "http_status": 400,
                "title": "Compliance Check Failed",
                "description": "The operation failed compliance checks.",
                "solution": "Review compliance requirements and try again",
                "example": {
                    "error": "Compliance check failed",
                    "code": "COMPLIANCE_CHECK_FAILED",
                    "details": "Risk score exceeds threshold"
                }
            },
            ErrorCode.KYC_REQUIRED.value: {
                "http_status": 400,
                "title": "KYC Required",
                "description": "KYC verification is required to perform this operation.",
                "solution": "Complete KYC verification process",
                "example": {
                    "error": "KYC required",
                    "code": "KYC_REQUIRED",
                    "details": "Account must be KYC verified for transfers"
                }
            },
            ErrorCode.KYC_VERIFICATION_FAILED.value: {
                "http_status": 400,
                "title": "KYC Verification Failed",
                "description": "KYC verification failed due to invalid or insufficient information.",
                "solution": "Review provided information and try again",
                "example": {
                    "error": "KYC verification failed",
                    "code": "KYC_VERIFICATION_FAILED",
                    "details": "Document verification failed"
                }
            },
            ErrorCode.SANCTIONS_HIT.value: {
                "http_status": 403,
                "title": "Sanctions Hit",
                "description": "The operation is blocked due to sanctions screening.",
                "solution": "Contact compliance team for review",
                "example": {
                    "error": "Sanctions hit",
                    "code": "SANCTIONS_HIT",
                    "details": "Entity matches sanctions list"
                }
            },
            ErrorCode.RATE_LIMIT_EXCEEDED.value: {
                "http_status": 429,
                "title": "Rate Limit Exceeded",
                "description": "Too many requests. Rate limit exceeded.",
                "solution": "Wait before making more requests or upgrade your plan",
                "example": {
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "details": {
                        "limit": 100,
                        "reset_time": "2024-01-01T01:00:00Z"
                    }
                }
            },
            ErrorCode.NETWORK_ERROR.value: {
                "http_status": 503,
                "title": "Network Error",
                "description": "Network connectivity issue occurred.",
                "solution": "Check your internet connection and try again",
                "example": {
                    "error": "Network error",
                    "code": "NETWORK_ERROR",
                    "details": "Unable to connect to blockchain network"
                }
            },
            ErrorCode.BLOCKCHAIN_UNAVAILABLE.value: {
                "http_status": 503,
                "title": "Blockchain Unavailable",
                "description": "The blockchain network is temporarily unavailable.",
                "solution": "Try again later or contact support",
                "example": {
                    "error": "Blockchain unavailable",
                    "code": "BLOCKCHAIN_UNAVAILABLE",
                    "details": "Stellar network is experiencing issues"
                }
            },
            ErrorCode.TRANSACTION_FAILED.value: {
                "http_status": 400,
                "title": "Transaction Failed",
                "description": "The blockchain transaction failed.",
                "solution": "Check transaction parameters and try again",
                "example": {
                    "error": "Transaction failed",
                    "code": "TRANSACTION_FAILED",
                    "details": "Transaction rejected by network"
                }
            },
            ErrorCode.INTERNAL_ERROR.value: {
                "http_status": 500,
                "title": "Internal Server Error",
                "description": "An unexpected error occurred on the server.",
                "solution": "Try again later or contact support if the issue persists",
                "example": {
                    "error": "Internal server error",
                    "code": "INTERNAL_ERROR",
                    "details": "An unexpected error occurred"
                }
            },
            ErrorCode.SERVICE_UNAVAILABLE.value: {
                "http_status": 503,
                "title": "Service Unavailable",
                "description": "The service is temporarily unavailable.",
                "solution": "Try again later or check status page",
                "example": {
                    "error": "Service unavailable",
                    "code": "SERVICE_UNAVAILABLE",
                    "details": "Service is under maintenance"
                }
            },
            ErrorCode.TIMEOUT.value: {
                "http_status": 504,
                "title": "Request Timeout",
                "description": "The request timed out.",
                "solution": "Try again with a shorter timeout or simpler request",
                "example": {
                    "error": "Request timeout",
                    "code": "TIMEOUT",
                    "details": "Request exceeded 30 second timeout"
                }
            }
        }
    
    @staticmethod
    def get_troubleshooting_guide() -> Dict[str, Any]:
        """Get comprehensive troubleshooting guide"""
        return {
            "common_issues": [
                {
                    "issue": "401 Unauthorized",
                    "causes": [
                        "Missing API key in request header",
                        "Invalid API key format",
                        "Expired API key"
                    ],
                    "solutions": [
                        "Add X-API-Key header to your request",
                        "Verify API key is correct",
                        "Generate new API key if expired"
                    ]
                },
                {
                    "issue": "400 Bad Request",
                    "causes": [
                        "Invalid request format",
                        "Missing required fields",
                        "Invalid parameter values"
                    ],
                    "solutions": [
                        "Check request body format (JSON)",
                        "Include all required fields",
                        "Verify parameter values and types"
                    ]
                },
                {
                    "issue": "429 Rate Limit Exceeded",
                    "causes": [
                        "Too many requests per minute",
                        "Exceeded daily quota"
                    ],
                    "solutions": [
                        "Implement request throttling",
                        "Upgrade to higher tier plan",
                        "Wait for rate limit reset"
                    ]
                },
                {
                    "issue": "500 Internal Server Error",
                    "causes": [
                        "Server-side error",
                        "Database connectivity issues",
                        "Blockchain network problems"
                    ],
                    "solutions": [
                        "Retry the request",
                        "Check API status page",
                        "Contact support if persistent"
                    ]
                }
            ],
            "best_practices": [
                "Always include proper error handling in your code",
                "Implement exponential backoff for retries",
                "Log error responses for debugging",
                "Use appropriate HTTP status codes",
                "Validate input data before sending requests",
                "Handle rate limiting gracefully",
                "Monitor API usage and quotas"
            ],
            "debugging_tips": [
                "Check the error response body for detailed information",
                "Verify request headers and format",
                "Test with curl or Postman first",
                "Enable request/response logging",
                "Check API documentation for examples",
                "Use the interactive API explorer in /docs"
            ]
        }
    
    @staticmethod
    def get_error_by_code(error_code: str) -> Dict[str, Any]:
        """Get specific error information by code"""
        all_errors = ErrorCodes.get_error_codes()
        return all_errors.get(error_code.upper(), {
            "http_status": 500,
            "title": "Unknown Error",
            "description": f"Unknown error code: {error_code}",
            "solution": "Contact support for assistance",
            "example": {
                "error": "Unknown error",
                "code": error_code,
                "details": "Error code not recognized"
            }
        })
    
    @staticmethod
    def get_errors_by_status_code(status_code: int) -> List[Dict[str, Any]]:
        """Get all errors for a specific HTTP status code"""
        all_errors = ErrorCodes.get_error_codes()
        return [
            {"code": code, **error_info}
            for code, error_info in all_errors.items()
            if error_info["http_status"] == status_code
        ]
