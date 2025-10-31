"""
Analytics endpoints for remittance flows and stablecoin tracking
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, Field
import structlog

from api.core.database import get_db
from api.services.analytics_service import AnalyticsService

logger = structlog.get_logger()
router = APIRouter()


# Pydantic models for request/response
class RemittanceFlowResponse(BaseModel):
    """Response model for remittance flow analytics"""
    from_country: str
    to_country: str
    from_region: Optional[str]
    to_region: Optional[str]
    asset_code: str
    network: str
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_senders: int
    unique_receivers: int
    avg_transaction_size: Optional[str]
    avg_transaction_size_usd: Optional[str]
    avg_fee: Optional[str]
    avg_fee_usd: Optional[str]
    avg_settlement_time: Optional[float]
    success_rate: Optional[float]
    period_start: str
    period_end: str
    period_type: str


class StablecoinAdoptionResponse(BaseModel):
    """Response model for stablecoin adoption analytics"""
    asset_code: str
    network: str
    country_code: Optional[str]
    region: Optional[str]
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_users: int
    avg_transaction_size: Optional[str]
    avg_transaction_size_usd: Optional[str]
    volume_growth_rate: Optional[float]
    user_growth_rate: Optional[float]
    period_start: str
    period_end: str
    period_type: str


class MerchantActivityResponse(BaseModel):
    """Response model for merchant activity analytics"""
    merchant_id: str
    merchant_name: Optional[str]
    merchant_type: str
    country_code: str
    region: Optional[str]
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_customers: int
    avg_transaction_size: Optional[str]
    avg_transaction_size_usd: Optional[str]
    stellar_volume: str
    hedera_volume: str
    stellar_transactions: int
    hedera_transactions: int
    period_start: str
    period_end: str
    period_type: str


class NetworkMetricsResponse(BaseModel):
    """Response model for network metrics"""
    network: str
    environment: str
    total_transactions: int
    total_volume: str
    total_volume_usd: str
    active_accounts: int
    new_accounts: int
    avg_transaction_fee: Optional[str]
    avg_transaction_fee_usd: Optional[str]
    avg_confirmation_time: Optional[float]
    success_rate: Optional[float]
    africa_transaction_count: int
    africa_volume: str
    africa_volume_usd: str
    period_start: str
    period_end: str
    period_type: str


@router.get("/remittance")
async def get_remittance_flows(
    from_country: Optional[str] = None,
    to_country: Optional[str] = None,
    from_region: Optional[str] = None,
    to_region: Optional[str] = None,
    asset_code: Optional[str] = None,
    network: Optional[str] = None,
    period_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "total_volume_usd",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive remittance flow analytics between countries/regions (AC1-10)"""
    try:
        # Validate parameters
        if limit > 1000:
            limit = 1000  # Cap limit for performance
        if limit < 1:
            limit = 1
        
        if offset < 0:
            offset = 0
        
        valid_sort_fields = ["total_volume_usd", "transaction_count", "period_start", "from_country", "to_country"]
        if sort_by not in valid_sort_fields:
            sort_by = "total_volume_usd"
        
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        # Parse date parameters
        from datetime import datetime
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        analytics_service = AnalyticsService(db)
        result = await analytics_service.get_remittance_flows(
            from_country=from_country,
            to_country=to_country,
            from_region=from_region,
            to_region=to_region,
            asset_code=asset_code,
            network=network,
            period_type=period_type,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get remittance flows", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get remittance flows: {str(e)}"
        )


@router.get("/stablecoin")
async def get_stablecoin_adoption(
    asset_code: Optional[str] = None,
    network: Optional[str] = None,
    country_code: Optional[str] = None,
    region: Optional[str] = None,
    period_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "total_volume_usd",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive stablecoin adoption analytics (AC1-10)"""
    try:
        # Validate parameters
        if limit > 1000:
            limit = 1000  # Cap limit for performance
        if limit < 1:
            limit = 1
        
        if offset < 0:
            offset = 0
        
        valid_sort_fields = ["total_volume_usd", "transaction_count", "unique_users", "period_start", "asset_code"]
        if sort_by not in valid_sort_fields:
            sort_by = "total_volume_usd"
        
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        # Parse date parameters
        from datetime import datetime
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        analytics_service = AnalyticsService(db)
        result = await analytics_service.get_stablecoin_adoption(
            asset_code=asset_code,
            network=network,
            country_code=country_code,
            region=region,
            period_type=period_type,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get stablecoin adoption", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stablecoin adoption: {str(e)}"
        )


@router.get("/merchants")
async def get_merchant_activity(
    merchant_type: Optional[str] = None,
    country_code: Optional[str] = None,
    network: Optional[str] = None,
    period_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "total_volume_usd",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive merchant activity analytics (AC1-10)"""
    try:
        # Validate parameters
        if limit > 1000:
            limit = 1000  # Cap limit for performance
        if limit < 1:
            limit = 1
        
        if offset < 0:
            offset = 0
        
        valid_sort_fields = ["total_volume_usd", "transaction_count", "unique_customers", "period_start", "merchant_type"]
        if sort_by not in valid_sort_fields:
            sort_by = "total_volume_usd"
        
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        # Parse date parameters
        from datetime import datetime
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        analytics_service = AnalyticsService(db)
        result = await analytics_service.get_merchant_activity(
            merchant_type=merchant_type,
            country_code=country_code,
            network=network,
            period_type=period_type,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get merchant activity", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get merchant activity: {str(e)}"
        )


@router.get("/network")
async def get_network_metrics(
    network: Optional[str] = None,
    period_type: str = "daily",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive network metrics and health data (AC1-10)"""
    try:
        # Validate parameters
        if limit > 1000:
            limit = 1000  # Cap limit for performance
        if limit < 1:
            limit = 1
        
        if offset < 0:
            offset = 0
        
        valid_sort_fields = ["timestamp", "total_transactions", "total_volume_usd", "success_rate", "throughput_tps"]
        if sort_by not in valid_sort_fields:
            sort_by = "timestamp"
        
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        # Parse date parameters
        from datetime import datetime
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        analytics_service = AnalyticsService(db)
        result = await analytics_service.get_network_metrics(
            network=network,
            period_type=period_type,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get network metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get network metrics: {str(e)}"
        )


@router.get("/dashboard")
async def get_dashboard_data(
    country_code: Optional[str] = None,
    region: Optional[str] = None,
    period_type: str = "monthly",
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive dashboard data"""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(
            country_code=country_code,
            region=region,
            period_type=period_type
        )
        
        return dashboard_data
        
    except Exception as e:
        logger.error("Failed to get dashboard data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard data: {str(e)}"
        )
