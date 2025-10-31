"""
Sandbox environment endpoints for testing and development
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import structlog

from api.core.database import get_db
from api.core.auth import require_api_key
from api.services.sandbox_service import SandboxService, SandboxEnvironment

logger = structlog.get_logger()
router = APIRouter()


@router.get("/stats")
async def get_sandbox_stats(
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get sandbox environment statistics"""
    try:
        sandbox_service = SandboxService(db)
        stats = await sandbox_service.get_sandbox_stats()
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error("Failed to get sandbox stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox stats: {str(e)}"
        )


@router.post("/accounts/generate")
async def generate_mock_accounts(
    count: int = Query(default=10, ge=1, le=100, description="Number of accounts to generate"),
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:write"]))
):
    """Generate mock accounts for sandbox testing"""
    try:
        sandbox_service = SandboxService(db)
        accounts = await sandbox_service.generate_mock_accounts(count)
        
        # In a real implementation, you would save these to the database
        # For now, we'll just return the generated accounts
        
        return {
            "success": True,
            "data": {
                "accounts": [
                    {
                        "id": account.id,
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
                        "metadata": account.metadata
                    }
                    for account in accounts
                ],
                "count": len(accounts),
                "generated_at": accounts[0].created_at.isoformat() if accounts else None
            }
        }
        
    except Exception as e:
        logger.error("Failed to generate mock accounts", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mock accounts: {str(e)}"
        )


@router.post("/transactions/generate")
async def generate_mock_transactions(
    account_ids: List[str] = Query(description="List of account IDs to generate transactions for"),
    count: int = Query(default=50, ge=1, le=1000, description="Number of transactions to generate"),
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:write"]))
):
    """Generate mock transactions for sandbox testing"""
    try:
        sandbox_service = SandboxService(db)
        transactions = await sandbox_service.generate_mock_transactions(account_ids, count)
        
        return {
            "success": True,
            "data": {
                "transactions": [
                    {
                        "id": tx.id,
                        "transaction_hash": tx.transaction_hash,
                        "network": tx.network,
                        "environment": tx.environment,
                        "transaction_type": tx.transaction_type,
                        "status": tx.status,
                        "from_account": tx.from_account,
                        "to_account": tx.to_account,
                        "asset_code": tx.asset_code,
                        "amount": tx.amount,
                        "amount_usd": tx.amount_usd,
                        "from_country": tx.from_country,
                        "to_country": tx.to_country,
                        "from_region": tx.from_region,
                        "to_region": tx.to_region,
                        "memo": tx.memo,
                        "fee": tx.fee,
                        "fee_usd": tx.fee_usd,
                        "created_at": tx.created_at.isoformat(),
                        "updated_at": tx.updated_at.isoformat(),
                        "ledger_time": tx.ledger_time.isoformat() if tx.ledger_time else None,
                        "compliance_status": tx.compliance_status,
                        "risk_score": tx.risk_score
                    }
                    for tx in transactions
                ],
                "count": len(transactions),
                "generated_at": transactions[0].created_at.isoformat() if transactions else None
            }
        }
        
    except Exception as e:
        logger.error("Failed to generate mock transactions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mock transactions: {str(e)}"
        )


@router.post("/analytics/generate")
async def generate_mock_analytics(
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:write"]))
):
    """Generate mock analytics data for sandbox testing"""
    try:
        sandbox_service = SandboxService(db)
        analytics_data = await sandbox_service.generate_mock_analytics_data()
        
        return {
            "success": True,
            "data": {
                "remittance_flows": [
                    {
                        "id": flow.id,
                        "from_country": flow.from_country,
                        "to_country": flow.to_country,
                        "from_region": flow.from_region,
                        "to_region": flow.to_region,
                        "asset_code": flow.asset_code,
                        "network": flow.network,
                        "total_volume": flow.total_volume,
                        "total_volume_usd": flow.total_volume_usd,
                        "transaction_count": flow.transaction_count,
                        "unique_senders": flow.unique_senders,
                        "unique_receivers": flow.unique_receivers,
                        "avg_transaction_size": flow.avg_transaction_size,
                        "avg_transaction_size_usd": flow.avg_transaction_size_usd,
                        "avg_fee": flow.avg_fee,
                        "avg_fee_usd": flow.avg_fee_usd,
                        "avg_settlement_time": flow.avg_settlement_time,
                        "success_rate": flow.success_rate,
                        "period_start": flow.period_start.isoformat(),
                        "period_end": flow.period_end.isoformat(),
                        "period_type": flow.period_type
                    }
                    for flow in analytics_data['remittance_flows']
                ],
                "stablecoin_adoption": [
                    {
                        "id": adoption.id,
                        "asset_code": adoption.asset_code,
                        "network": adoption.network,
                        "country_code": adoption.country_code,
                        "region": adoption.region,
                        "total_volume": adoption.total_volume,
                        "total_volume_usd": adoption.total_volume_usd,
                        "transaction_count": adoption.transaction_count,
                        "unique_users": adoption.unique_users,
                        "avg_transaction_size": adoption.avg_transaction_size,
                        "avg_transaction_size_usd": adoption.avg_transaction_size_usd,
                        "volume_growth_rate": adoption.volume_growth_rate,
                        "user_growth_rate": adoption.user_growth_rate,
                        "period_start": adoption.period_start.isoformat(),
                        "period_end": adoption.period_end.isoformat(),
                        "period_type": adoption.period_type
                    }
                    for adoption in analytics_data['stablecoin_adoption']
                ],
                "merchant_activity": [
                    {
                        "id": activity.id,
                        "merchant_id": activity.merchant_id,
                        "merchant_name": activity.merchant_name,
                        "merchant_type": activity.merchant_type,
                        "country_code": activity.country_code,
                        "region": activity.region,
                        "total_volume": activity.total_volume,
                        "total_volume_usd": activity.total_volume_usd,
                        "transaction_count": activity.transaction_count,
                        "unique_customers": activity.unique_customers,
                        "avg_transaction_size": activity.avg_transaction_size,
                        "avg_transaction_size_usd": activity.avg_transaction_size_usd,
                        "stellar_volume": activity.stellar_volume,
                        "hedera_volume": activity.hedera_volume,
                        "stellar_transactions": activity.stellar_transactions,
                        "hedera_transactions": activity.hedera_transactions,
                        "period_start": activity.period_start.isoformat(),
                        "period_end": activity.period_end.isoformat(),
                        "period_type": activity.period_type
                    }
                    for activity in analytics_data['merchant_activity']
                ],
                "network_metrics": [
                    {
                        "id": metric.id,
                        "network": metric.network,
                        "environment": metric.environment,
                        "total_transactions": metric.total_transactions,
                        "total_volume": metric.total_volume,
                        "total_volume_usd": metric.total_volume_usd,
                        "active_accounts": metric.active_accounts,
                        "new_accounts": metric.new_accounts,
                        "avg_transaction_fee": metric.avg_transaction_fee,
                        "avg_transaction_fee_usd": metric.avg_transaction_fee_usd,
                        "avg_confirmation_time": metric.avg_confirmation_time,
                        "success_rate": metric.success_rate,
                        "africa_transaction_count": metric.africa_transaction_count,
                        "africa_volume": metric.africa_volume,
                        "africa_volume_usd": metric.africa_volume_usd,
                        "period_start": metric.period_start.isoformat(),
                        "period_end": metric.period_end.isoformat(),
                        "period_type": metric.period_type
                    }
                    for metric in analytics_data['network_metrics']
                ]
            }
        }
        
    except Exception as e:
        logger.error("Failed to generate mock analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mock analytics: {str(e)}"
        )


@router.post("/compliance/generate")
async def generate_mock_compliance_data(
    account_ids: List[str] = Query(description="List of account IDs for KYC verifications"),
    entity_ids: List[str] = Query(description="List of entity IDs for compliance flags"),
    kyc_count: int = Query(default=20, ge=1, le=100, description="Number of KYC verifications to generate"),
    flag_count: int = Query(default=15, ge=1, le=100, description="Number of compliance flags to generate"),
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:write"]))
):
    """Generate mock compliance data for sandbox testing"""
    try:
        sandbox_service = SandboxService(db)
        
        kyc_verifications = await sandbox_service.generate_mock_kyc_verifications(account_ids, kyc_count)
        compliance_flags = await sandbox_service.generate_mock_compliance_flags(entity_ids, flag_count)
        
        return {
            "success": True,
            "data": {
                "kyc_verifications": [
                    {
                        "id": kyc.id,
                        "verification_id": kyc.verification_id,
                        "account_id": kyc.account_id,
                        "network": kyc.network,
                        "verification_type": kyc.verification_type,
                        "verification_status": kyc.verification_status,
                        "provider": kyc.provider,
                        "verification_score": kyc.verification_score,
                        "risk_level": kyc.risk_level,
                        "verification_notes": kyc.verification_notes,
                        "created_at": kyc.created_at.isoformat(),
                        "updated_at": kyc.updated_at.isoformat(),
                        "verified_at": kyc.verified_at.isoformat() if kyc.verified_at else None,
                        "expires_at": kyc.expires_at.isoformat() if kyc.expires_at else None
                    }
                    for kyc in kyc_verifications
                ],
                "compliance_flags": [
                    {
                        "id": flag.id,
                        "entity_type": flag.entity_type,
                        "entity_id": flag.entity_id,
                        "network": flag.network,
                        "flag_type": flag.flag_type,
                        "flag_severity": flag.flag_severity,
                        "flag_status": flag.flag_status,
                        "flag_reason": flag.flag_reason,
                        "risk_score": flag.risk_score,
                        "country_code": flag.country_code,
                        "region": flag.region,
                        "resolved_by": flag.resolved_by,
                        "resolution_notes": flag.resolution_notes,
                        "created_at": flag.created_at.isoformat(),
                        "updated_at": flag.updated_at.isoformat(),
                        "resolved_at": flag.resolved_at.isoformat() if flag.resolved_at else None
                    }
                    for flag in compliance_flags
                ],
                "counts": {
                    "kyc_verifications": len(kyc_verifications),
                    "compliance_flags": len(compliance_flags)
                }
            }
        }
        
    except Exception as e:
        logger.error("Failed to generate mock compliance data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mock compliance data: {str(e)}"
        )


@router.post("/reset")
async def reset_sandbox_data(
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:admin"]))
):
    """Reset all sandbox data to initial state"""
    try:
        sandbox_service = SandboxService(db)
        result = await sandbox_service.reset_sandbox_data()
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error("Failed to reset sandbox data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset sandbox data: {str(e)}"
        )


@router.get("/scenarios")
async def get_test_scenarios(
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get available test scenarios for sandbox environment"""
    try:
        scenarios = {
            "basic_integration": {
                "name": "Basic Integration Test",
                "description": "Test basic account creation and transfer functionality",
                "steps": [
                    "Create test accounts",
                    "Generate test transactions",
                    "Verify account balances",
                    "Test transfer operations"
                ],
                "estimated_duration": "5-10 minutes"
            },
            "compliance_testing": {
                "name": "Compliance Testing",
                "description": "Test KYC verification and compliance flagging",
                "steps": [
                    "Generate KYC verifications",
                    "Create compliance flags",
                    "Test flag resolution",
                    "Verify compliance reports"
                ],
                "estimated_duration": "10-15 minutes"
            },
            "analytics_testing": {
                "name": "Analytics Testing",
                "description": "Test analytics and reporting functionality",
                "steps": [
                    "Generate analytics data",
                    "Test dashboard endpoints",
                    "Verify remittance flows",
                    "Test stablecoin adoption metrics"
                ],
                "estimated_duration": "15-20 minutes"
            },
            "stress_testing": {
                "name": "Stress Testing",
                "description": "Test system performance under load",
                "steps": [
                    "Generate large volume of accounts",
                    "Create many transactions",
                    "Test rate limiting",
                    "Monitor system performance"
                ],
                "estimated_duration": "20-30 minutes"
            },
            "error_handling": {
                "name": "Error Handling Testing",
                "description": "Test error scenarios and edge cases",
                "steps": [
                    "Test invalid API keys",
                    "Test malformed requests",
                    "Test rate limit scenarios",
                    "Verify error responses"
                ],
                "estimated_duration": "10-15 minutes"
            }
        }
        
        return {
            "success": True,
            "data": {
                "scenarios": scenarios,
                "total_scenarios": len(scenarios),
                "usage_instructions": {
                    "step_1": "Choose a test scenario based on your testing needs",
                    "step_2": "Generate the required mock data using the appropriate endpoints",
                    "step_3": "Follow the scenario steps to test your integration",
                    "step_4": "Reset sandbox data when finished testing"
                }
            }
        }
        
    except Exception as e:
        logger.error("Failed to get test scenarios", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get test scenarios: {str(e)}"
        )


@router.get("/rate-limits")
async def get_sandbox_rate_limits(
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get sandbox environment rate limiting information"""
    try:
        rate_limits = {
            "sandbox_tier": {
                "name": "Sandbox Tier",
                "description": "Rate limits for sandbox environment",
                "limits": {
                    "requests_per_minute": 1000,
                    "requests_per_hour": 60000,
                    "requests_per_day": 1000000,
                    "burst_limit": 1500
                },
                "features": [
                    "Unlimited mock data generation",
                    "Full API access for testing",
                    "Rate limit testing capabilities",
                    "Real-time rate limit monitoring"
                ]
            },
            "testing_guidelines": {
                "rate_limit_testing": "Use sandbox to test rate limiting behavior",
                "monitoring": "Monitor rate limit headers in responses",
                "best_practices": "Implement proper retry logic in your application"
            },
            "headers": {
                "X-RateLimit-Limit": "The rate limit ceiling for the given request",
                "X-RateLimit-Remaining": "The number of requests left in the current window",
                "X-RateLimit-Reset": "The time at which the current window resets",
                "Retry-After": "Number of seconds to wait before retrying (on 429 responses)"
            }
        }
        
        return {
            "success": True,
            "data": rate_limits
        }
        
    except Exception as e:
        logger.error("Failed to get sandbox rate limits", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox rate limits: {str(e)}"
        )


@router.post("/initialize")
async def initialize_sandbox_environment(
    environment: str = Query(default="sandbox", description="Sandbox environment type"),
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:admin"]))
):
    """Initialize sandbox environment with comprehensive mock data"""
    try:
        sandbox_service = SandboxService(db)
        
        # Validate environment
        try:
            env_enum = SandboxEnvironment(environment)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid environment '{environment}'. Must be one of: {[e.value for e in SandboxEnvironment]}"
            )
        
        result = await sandbox_service.initialize_sandbox_environment(env_enum)
        
        return {
            "success": True,
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to initialize sandbox environment", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize sandbox environment: {str(e)}"
        )


@router.get("/scenarios/{scenario_id}")
async def get_test_scenario(
    scenario_id: str,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get specific test scenario details"""
    try:
        sandbox_service = SandboxService(db)
        result = await sandbox_service.get_test_scenario(scenario_id)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["message"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get test scenario", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get test scenario: {str(e)}"
        )


@router.post("/scenarios/{scenario_id}/execute")
async def execute_test_scenario(
    scenario_id: str,
    params: Dict[str, Any] = None,
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:write"]))
):
    """Execute a specific test scenario"""
    try:
        sandbox_service = SandboxService(db)
        result = await sandbox_service.execute_test_scenario(scenario_id, params)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to execute test scenario", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute test scenario: {str(e)}"
        )


@router.get("/analytics")
async def get_sandbox_usage_analytics(
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get sandbox usage analytics and monitoring data"""
    try:
        sandbox_service = SandboxService(db)
        result = await sandbox_service.get_sandbox_usage_analytics()
        
        return result
        
    except Exception as e:
        logger.error("Failed to get sandbox analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox analytics: {str(e)}"
        )


@router.patch("/config")
async def update_sandbox_config(
    config_updates: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:admin"]))
):
    """Update sandbox configuration"""
    try:
        sandbox_service = SandboxService(db)
        result = await sandbox_service.update_sandbox_config(config_updates)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update sandbox config", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update sandbox config: {str(e)}"
        )


@router.get("/health")
async def get_sandbox_health(
    db: AsyncSession = Depends(get_db),
    auth: Dict[str, Any] = Depends(require_api_key(["sandbox:read"]))
):
    """Get sandbox environment health status"""
    try:
        sandbox_service = SandboxService(db)
        
        # Get basic stats
        stats = await sandbox_service.get_sandbox_stats()
        analytics = await sandbox_service.get_sandbox_usage_analytics()
        
        # Determine health status
        is_healthy = (
            stats.get("success", False) and 
            analytics.get("success", False) and
            analytics["data"]["current_status"] == "active"
        )
        
        health_status = {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "sandbox_service": "healthy" if stats.get("success", False) else "unhealthy",
                "analytics_service": "healthy" if analytics.get("success", False) else "unhealthy",
                "mock_data_generation": "healthy",
                "test_scenarios": "healthy"
            },
            "stats": stats.get("data", {}) if stats.get("success", False) else {},
            "analytics": analytics.get("data", {}) if analytics.get("success", False) else {}
        }
        
        return {
            "success": True,
            "data": health_status
        }
        
    except Exception as e:
        logger.error("Failed to get sandbox health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox health: {str(e)}"
        )
