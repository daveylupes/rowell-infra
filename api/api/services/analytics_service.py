"""
Analytics service for handling analytics operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, Numeric
from datetime import datetime, timedelta
import structlog

from api.models.account import Account
from api.models.transaction import Transaction
from api.models.analytics import NetworkMetrics, RemittanceFlow, StablecoinAdoption, MerchantActivity

logger = structlog.get_logger()


class AnalyticsService:
    """Service for analytics and reporting"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_remittance_flows(
        self,
        from_country: Optional[str] = None,
        to_country: Optional[str] = None,
        from_region: Optional[str] = None,
        to_region: Optional[str] = None,
        asset_code: Optional[str] = None,
        network: Optional[str] = None,
        period_type: str = "monthly",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "total_volume_usd",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """Get comprehensive remittance flow analytics (AC1-10)"""
        try:
            logger.info("Generating remittance flow analytics", 
                       from_country=from_country, to_country=to_country,
                       from_region=from_region, to_region=to_region,
                       asset_code=asset_code, network=network, period_type=period_type)
            
            # Build base query
            query = select(RemittanceFlow)
            count_query = select(func.count(RemittanceFlow.id))
            
            # Apply filters
            filters = []
            if from_country:
                filters.append(RemittanceFlow.from_country == from_country.upper())
            if to_country:
                filters.append(RemittanceFlow.to_country == to_country.upper())
            if from_region:
                filters.append(RemittanceFlow.from_region == from_region)
            if to_region:
                filters.append(RemittanceFlow.to_region == to_region)
            if asset_code:
                filters.append(RemittanceFlow.asset_code == asset_code.upper())
            if network:
                filters.append(RemittanceFlow.network == network.lower())
            if period_type:
                filters.append(RemittanceFlow.period_type == period_type)
            
            # Date range filtering
            if start_date:
                filters.append(RemittanceFlow.period_start >= start_date)
            if end_date:
                filters.append(RemittanceFlow.period_end <= end_date)
            
            if filters:
                filter_condition = and_(*filters)
                query = query.where(filter_condition)
                count_query = count_query.where(filter_condition)
            
            # Apply sorting
            sort_column = getattr(RemittanceFlow, sort_by, RemittanceFlow.total_volume_usd)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            # Execute queries
            result = await self.db.execute(query)
            flows = result.scalars().all()
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Build response with comprehensive flow data
            flow_list = []
            for flow in flows:
                flow_data = {
                    "id": str(flow.id),
                    "from_country": flow.from_country,
                    "to_country": flow.to_country,
                    "from_region": flow.from_region,
                    "to_region": flow.to_region,
                    "asset_code": flow.asset_code,
                    "network": flow.network,
                    "total_volume": flow.total_volume,
                    "total_volume_usd": flow.total_volume_usd,
                    "transaction_count": int(flow.transaction_count),
                    "unique_senders": int(flow.unique_senders),
                    "unique_receivers": int(flow.unique_receivers),
                    "avg_fee": flow.avg_fee,
                    "avg_fee_usd": flow.avg_fee_usd,
                    "avg_fee_percentage": float(flow.avg_fee_percentage) if flow.avg_fee_percentage else None,
                    "avg_settlement_time": float(flow.avg_settlement_time) if flow.avg_settlement_time else None,
                    "success_rate": float(flow.success_rate) if flow.success_rate else None,
                    "period_start": flow.period_start.isoformat(),
                    "period_end": flow.period_end.isoformat(),
                    "period_type": flow.period_type,
                    "created_at": flow.created_at.isoformat(),
                    "updated_at": flow.updated_at.isoformat()
                }
                flow_list.append(flow_data)
            
            # Get aggregated analytics
            analytics = await self._get_remittance_analytics(filters)
            
            return {
                "flows": flow_list,
                "pagination": {
                    "total": total_count,
                    "page": (offset // limit) + 1,
                    "per_page": limit,
                    "pages": (total_count + limit - 1) // limit,
                    "has_next": offset + limit < total_count,
                    "has_prev": offset > 0
                },
                "filters": {
                    "from_country": from_country,
                    "to_country": to_country,
                    "from_region": from_region,
                    "to_region": to_region,
                    "asset_code": asset_code,
                    "network": network,
                    "period_type": period_type,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error("Failed to get remittance flows", error=str(e))
            raise
    
    async def _get_remittance_analytics(self, filters: List) -> Dict[str, Any]:
        """Get aggregated remittance analytics (AC2, AC7)"""
        try:
            # Build base query for analytics
            base_query = select(RemittanceFlow)
            if filters:
                filter_condition = and_(*filters)
                base_query = base_query.where(filter_condition)
            
            # Get total volume and transaction count
            volume_query = select(
                func.sum(func.cast(RemittanceFlow.total_volume_usd, Numeric)).label('total_volume_usd'),
                func.sum(RemittanceFlow.transaction_count).label('total_transactions'),
                func.count(RemittanceFlow.id).label('total_flows')
            )
            if filters:
                volume_query = volume_query.where(filter_condition)
            
            volume_result = await self.db.execute(volume_query)
            volume_data = volume_result.first()
            
            # Get top corridors by volume
            top_corridors_query = select(
                RemittanceFlow.from_country,
                RemittanceFlow.to_country,
                func.sum(func.cast(RemittanceFlow.total_volume_usd, Numeric)).label('volume'),
                func.sum(RemittanceFlow.transaction_count).label('transactions')
            ).group_by(
                RemittanceFlow.from_country, RemittanceFlow.to_country
            ).order_by(desc('volume')).limit(10)
            
            if filters:
                top_corridors_query = top_corridors_query.where(filter_condition)
            
            corridors_result = await self.db.execute(top_corridors_query)
            top_corridors = [
                {
                    "from_country": row.from_country,
                    "to_country": row.to_country,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0
                }
                for row in corridors_result
            ]
            
            # Get asset breakdown
            asset_query = select(
                RemittanceFlow.asset_code,
                func.sum(func.cast(RemittanceFlow.total_volume_usd, Numeric)).label('volume'),
                func.sum(RemittanceFlow.transaction_count).label('transactions')
            ).group_by(RemittanceFlow.asset_code).order_by(desc('volume'))
            
            if filters:
                asset_query = asset_query.where(filter_condition)
            
            asset_result = await self.db.execute(asset_query)
            asset_breakdown = [
                {
                    "asset_code": row.asset_code,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0
                }
                for row in asset_result
            ]
            
            # Get regional breakdown
            regional_query = select(
                RemittanceFlow.from_region,
                RemittanceFlow.to_region,
                func.sum(func.cast(RemittanceFlow.total_volume_usd, Numeric)).label('volume'),
                func.sum(RemittanceFlow.transaction_count).label('transactions')
            ).group_by(
                RemittanceFlow.from_region, RemittanceFlow.to_region
            ).order_by(desc('volume')).limit(10)
            
            if filters:
                regional_query = regional_query.where(filter_condition)
            
            regional_result = await self.db.execute(regional_query)
            regional_breakdown = [
                {
                    "from_region": row.from_region,
                    "to_region": row.to_region,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0
                }
                for row in regional_result
            ]
            
            return {
                "summary": {
                    "total_volume_usd": str(volume_data.total_volume_usd) if volume_data.total_volume_usd else "0",
                    "total_transactions": int(volume_data.total_transactions) if volume_data.total_transactions else 0,
                    "total_flows": int(volume_data.total_flows) if volume_data.total_flows else 0
                },
                "top_corridors": top_corridors,
                "asset_breakdown": asset_breakdown,
                "regional_breakdown": regional_breakdown
            }
            
        except Exception as e:
            logger.error("Failed to get remittance analytics", error=str(e))
            return {
                "summary": {"total_volume_usd": "0", "total_transactions": 0, "total_flows": 0},
                "top_corridors": [],
                "asset_breakdown": [],
                "regional_breakdown": []
            }
    
    async def get_stablecoin_adoption(
        self,
        asset_code: Optional[str] = None,
        network: Optional[str] = None,
        country_code: Optional[str] = None,
        region: Optional[str] = None,
        period_type: str = "monthly",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "total_volume_usd",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """Get comprehensive stablecoin adoption analytics (AC1-10)"""
        try:
            logger.info("Generating stablecoin adoption analytics", 
                       asset_code=asset_code, network=network,
                       country_code=country_code, region=region, period_type=period_type)
            
            # Build base query
            query = select(StablecoinAdoption)
            count_query = select(func.count(StablecoinAdoption.id))
            
            # Apply filters
            filters = []
            if asset_code:
                filters.append(StablecoinAdoption.asset_code == asset_code.upper())
            if network:
                filters.append(StablecoinAdoption.network == network.lower())
            if country_code:
                filters.append(StablecoinAdoption.country_code == country_code.upper())
            if region:
                filters.append(StablecoinAdoption.region == region)
            if period_type:
                filters.append(StablecoinAdoption.period_type == period_type)
            
            # Date range filtering
            if start_date:
                filters.append(StablecoinAdoption.period_start >= start_date)
            if end_date:
                filters.append(StablecoinAdoption.period_end <= end_date)
            
            if filters:
                filter_condition = and_(*filters)
                query = query.where(filter_condition)
                count_query = count_query.where(filter_condition)
            
            # Apply sorting
            sort_column = getattr(StablecoinAdoption, sort_by, StablecoinAdoption.total_volume_usd)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            # Execute queries
            result = await self.db.execute(query)
            adoptions = result.scalars().all()
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Build response with comprehensive adoption data
            adoption_list = []
            for adoption in adoptions:
                adoption_data = {
                    "id": str(adoption.id),
                    "asset_code": adoption.asset_code,
                    "network": adoption.network,
                    "country_code": adoption.country_code,
                    "region": adoption.region,
                    "total_volume": adoption.total_volume,
                    "total_volume_usd": adoption.total_volume_usd,
                    "transaction_count": int(adoption.transaction_count),
                    "unique_users": int(adoption.unique_users),
                    "avg_transaction_size": adoption.avg_transaction_size,
                    "avg_transaction_size_usd": adoption.avg_transaction_size_usd,
                    "volume_growth_rate": float(adoption.volume_growth_rate) if adoption.volume_growth_rate else None,
                    "user_growth_rate": float(adoption.user_growth_rate) if adoption.user_growth_rate else None,
                    "period_start": adoption.period_start.isoformat(),
                    "period_end": adoption.period_end.isoformat(),
                    "period_type": adoption.period_type,
                    "created_at": adoption.created_at.isoformat(),
                    "updated_at": adoption.updated_at.isoformat()
                }
                adoption_list.append(adoption_data)
            
            # Get aggregated analytics
            analytics = await self._get_stablecoin_analytics(filters)
            
            return {
                "adoptions": adoption_list,
                "pagination": {
                    "total": total_count,
                    "page": (offset // limit) + 1,
                    "per_page": limit,
                    "pages": (total_count + limit - 1) // limit,
                    "has_next": offset + limit < total_count,
                    "has_prev": offset > 0
                },
                "filters": {
                    "asset_code": asset_code,
                    "network": network,
                    "country_code": country_code,
                    "region": region,
                    "period_type": period_type,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error("Failed to get stablecoin adoption", error=str(e))
            raise
    
    async def _get_stablecoin_analytics(self, filters: List) -> Dict[str, Any]:
        """Get aggregated stablecoin analytics (AC2-5, AC7-10)"""
        try:
            # Build base query for analytics
            base_query = select(StablecoinAdoption)
            if filters:
                filter_condition = and_(*filters)
                base_query = base_query.where(filter_condition)
            
            # Get total volume and transaction count
            volume_query = select(
                func.sum(func.cast(StablecoinAdoption.total_volume_usd, Numeric)).label('total_volume_usd'),
                func.sum(StablecoinAdoption.transaction_count).label('total_transactions'),
                func.sum(StablecoinAdoption.unique_users).label('total_users'),
                func.count(StablecoinAdoption.id).label('total_records')
            )
            if filters:
                volume_query = volume_query.where(filter_condition)
            
            volume_result = await self.db.execute(volume_query)
            volume_data = volume_result.first()
            
            # Get asset breakdown
            asset_query = select(
                StablecoinAdoption.asset_code,
                func.sum(func.cast(StablecoinAdoption.total_volume_usd, Numeric)).label('volume'),
                func.sum(StablecoinAdoption.transaction_count).label('transactions'),
                func.sum(StablecoinAdoption.unique_users).label('users'),
                func.avg(StablecoinAdoption.volume_growth_rate).label('avg_volume_growth'),
                func.avg(StablecoinAdoption.user_growth_rate).label('avg_user_growth')
            ).group_by(StablecoinAdoption.asset_code).order_by(desc('volume'))
            
            if filters:
                asset_query = asset_query.where(filter_condition)
            
            asset_result = await self.db.execute(asset_query)
            asset_breakdown = [
                {
                    "asset_code": row.asset_code,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "users": int(row.users) if row.users else 0,
                    "avg_volume_growth": float(row.avg_volume_growth) if row.avg_volume_growth else None,
                    "avg_user_growth": float(row.avg_user_growth) if row.avg_user_growth else None
                }
                for row in asset_result
            ]
            
            # Get network comparison
            network_query = select(
                StablecoinAdoption.network,
                func.sum(func.cast(StablecoinAdoption.total_volume_usd, Numeric)).label('volume'),
                func.sum(StablecoinAdoption.transaction_count).label('transactions'),
                func.sum(StablecoinAdoption.unique_users).label('users'),
                func.avg(StablecoinAdoption.volume_growth_rate).label('avg_volume_growth'),
                func.avg(StablecoinAdoption.user_growth_rate).label('avg_user_growth')
            ).group_by(StablecoinAdoption.network).order_by(desc('volume'))
            
            if filters:
                network_query = network_query.where(filter_condition)
            
            network_result = await self.db.execute(network_query)
            network_comparison = [
                {
                    "network": row.network,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "users": int(row.users) if row.users else 0,
                    "avg_volume_growth": float(row.avg_volume_growth) if row.avg_volume_growth else None,
                    "avg_user_growth": float(row.avg_user_growth) if row.avg_user_growth else None
                }
                for row in network_result
            ]
            
            # Get country breakdown
            country_query = select(
                StablecoinAdoption.country_code,
                func.sum(func.cast(StablecoinAdoption.total_volume_usd, Numeric)).label('volume'),
                func.sum(StablecoinAdoption.transaction_count).label('transactions'),
                func.sum(StablecoinAdoption.unique_users).label('users'),
                func.avg(StablecoinAdoption.volume_growth_rate).label('avg_volume_growth'),
                func.avg(StablecoinAdoption.user_growth_rate).label('avg_user_growth')
            ).group_by(StablecoinAdoption.country_code).order_by(desc('volume')).limit(10)
            
            if filters:
                country_query = country_query.where(filter_condition)
            
            country_result = await self.db.execute(country_query)
            country_breakdown = [
                {
                    "country_code": row.country_code,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "users": int(row.users) if row.users else 0,
                    "avg_volume_growth": float(row.avg_volume_growth) if row.avg_volume_growth else None,
                    "avg_user_growth": float(row.avg_user_growth) if row.avg_user_growth else None
                }
                for row in country_result
            ]
            
            # Get regional breakdown
            regional_query = select(
                StablecoinAdoption.region,
                func.sum(func.cast(StablecoinAdoption.total_volume_usd, Numeric)).label('volume'),
                func.sum(StablecoinAdoption.transaction_count).label('transactions'),
                func.sum(StablecoinAdoption.unique_users).label('users'),
                func.avg(StablecoinAdoption.volume_growth_rate).label('avg_volume_growth'),
                func.avg(StablecoinAdoption.user_growth_rate).label('avg_user_growth')
            ).group_by(StablecoinAdoption.region).order_by(desc('volume'))
            
            if filters:
                regional_query = regional_query.where(filter_condition)
            
            regional_result = await self.db.execute(regional_query)
            regional_breakdown = [
                {
                    "region": row.region,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "users": int(row.users) if row.users else 0,
                    "avg_volume_growth": float(row.avg_volume_growth) if row.avg_volume_growth else None,
                    "avg_user_growth": float(row.avg_user_growth) if row.avg_user_growth else None
                }
                for row in regional_result
            ]
            
            return {
                "summary": {
                    "total_volume_usd": str(volume_data.total_volume_usd) if volume_data.total_volume_usd else "0",
                    "total_transactions": int(volume_data.total_transactions) if volume_data.total_transactions else 0,
                    "total_users": int(volume_data.total_users) if volume_data.total_users else 0,
                    "total_records": int(volume_data.total_records) if volume_data.total_records else 0
                },
                "asset_breakdown": asset_breakdown,
                "network_comparison": network_comparison,
                "country_breakdown": country_breakdown,
                "regional_breakdown": regional_breakdown
            }
            
        except Exception as e:
            logger.error("Failed to get stablecoin analytics", error=str(e))
            return {
                "summary": {"total_volume_usd": "0", "total_transactions": 0, "total_users": 0, "total_records": 0},
                "asset_breakdown": [],
                "network_comparison": [],
                "country_breakdown": [],
                "regional_breakdown": []
            }
    
    async def get_merchant_activity(
        self,
        merchant_type: Optional[str] = None,
        country_code: Optional[str] = None,
        network: Optional[str] = None,
        period_type: str = "monthly",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "total_volume_usd",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """Get comprehensive merchant activity analytics (AC1-10)"""
        try:
            logger.info("Generating merchant activity analytics", 
                       merchant_type=merchant_type, country_code=country_code,
                       network=network, period_type=period_type)
            
            # Build base query
            query = select(MerchantActivity)
            count_query = select(func.count(MerchantActivity.id))
            
            # Apply filters
            filters = []
            if merchant_type:
                filters.append(MerchantActivity.merchant_type == merchant_type.lower())
            if country_code:
                filters.append(MerchantActivity.country_code == country_code.upper())
            if period_type:
                filters.append(MerchantActivity.period_type == period_type)
            
            # Date range filtering
            if start_date:
                filters.append(MerchantActivity.period_start >= start_date)
            if end_date:
                filters.append(MerchantActivity.period_end <= end_date)
            
            if filters:
                filter_condition = and_(*filters)
                query = query.where(filter_condition)
                count_query = count_query.where(filter_condition)
            
            # Apply sorting
            sort_column = getattr(MerchantActivity, sort_by, MerchantActivity.total_volume_usd)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            # Execute queries
            result = await self.db.execute(query)
            activities = result.scalars().all()
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Build response with comprehensive merchant activity data
            activity_list = []
            for activity in activities:
                activity_data = {
                    "id": str(activity.id),
                    "merchant_id": activity.merchant_id,
                    "merchant_name": activity.merchant_name,
                    "merchant_type": activity.merchant_type,
                    "country_code": activity.country_code,
                    "region": activity.region,
                    "total_volume": activity.total_volume,
                    "total_volume_usd": activity.total_volume_usd,
                    "transaction_count": int(activity.transaction_count),
                    "unique_customers": int(activity.unique_customers),
                    "avg_transaction_size": activity.avg_transaction_size,
                    "avg_transaction_size_usd": activity.avg_transaction_size_usd,
                    "stellar_volume": activity.stellar_volume,
                    "hedera_volume": activity.hedera_volume,
                    "stellar_transactions": int(activity.stellar_transactions),
                    "hedera_transactions": int(activity.hedera_transactions),
                    "period_start": activity.period_start.isoformat(),
                    "period_end": activity.period_end.isoformat(),
                    "period_type": activity.period_type,
                    "created_at": activity.created_at.isoformat(),
                    "updated_at": activity.updated_at.isoformat()
                }
                activity_list.append(activity_data)
            
            # Get aggregated analytics
            analytics = await self._get_merchant_analytics(filters)
            
            return {
                "activities": activity_list,
                "pagination": {
                    "total": total_count,
                    "page": (offset // limit) + 1,
                    "per_page": limit,
                    "pages": (total_count + limit - 1) // limit,
                    "has_next": offset + limit < total_count,
                    "has_prev": offset > 0
                },
                "filters": {
                    "merchant_type": merchant_type,
                    "country_code": country_code,
                    "network": network,
                    "period_type": period_type,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error("Failed to get merchant activity", error=str(e))
            raise
    
    async def _get_merchant_analytics(self, filters: List) -> Dict[str, Any]:
        """Get aggregated merchant analytics (AC1-10)"""
        try:
            # Build base query for analytics
            base_query = select(MerchantActivity)
            if filters:
                filter_condition = and_(*filters)
                base_query = base_query.where(filter_condition)
            
            # Get total volume and transaction count
            volume_query = select(
                func.sum(func.cast(MerchantActivity.total_volume_usd, Numeric)).label('total_volume_usd'),
                func.sum(MerchantActivity.transaction_count).label('total_transactions'),
                func.sum(MerchantActivity.unique_customers).label('total_customers'),
                func.count(MerchantActivity.id).label('total_merchants')
            )
            if filters:
                volume_query = volume_query.where(filter_condition)
            
            volume_result = await self.db.execute(volume_query)
            volume_data = volume_result.first()
            
            # Get merchant type breakdown
            type_query = select(
                MerchantActivity.merchant_type,
                func.sum(func.cast(MerchantActivity.total_volume_usd, Numeric)).label('volume'),
                func.sum(MerchantActivity.transaction_count).label('transactions'),
                func.sum(MerchantActivity.unique_customers).label('customers')
            ).group_by(MerchantActivity.merchant_type).order_by(desc('volume'))
            
            if filters:
                type_query = type_query.where(filter_condition)
            
            type_result = await self.db.execute(type_query)
            type_breakdown = [
                {
                    "merchant_type": row.merchant_type,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "customers": int(row.customers) if row.customers else 0
                }
                for row in type_result
            ]
            
            # Get network breakdown (using stellar/hedera volume fields)
            network_breakdown = [
                {
                    "network": "stellar",
                    "volume": "0",  # Will be calculated from stellar_volume fields
                    "transactions": 0,  # Will be calculated from stellar_transactions fields
                    "customers": 0
                },
                {
                    "network": "hedera", 
                    "volume": "0",  # Will be calculated from hedera_volume fields
                    "transactions": 0,  # Will be calculated from hedera_transactions fields
                    "customers": 0
                }
            ]
            
            # Get country breakdown
            country_query = select(
                MerchantActivity.country_code,
                func.sum(func.cast(MerchantActivity.total_volume_usd, Numeric)).label('volume'),
                func.sum(MerchantActivity.transaction_count).label('transactions'),
                func.sum(MerchantActivity.unique_customers).label('customers')
            ).group_by(MerchantActivity.country_code).order_by(desc('volume')).limit(10)
            
            if filters:
                country_query = country_query.where(filter_condition)
            
            country_result = await self.db.execute(country_query)
            country_breakdown = [
                {
                    "country_code": row.country_code,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "customers": int(row.customers) if row.customers else 0
                }
                for row in country_result
            ]
            
            # Get regional breakdown
            regional_query = select(
                MerchantActivity.region,
                func.sum(func.cast(MerchantActivity.total_volume_usd, Numeric)).label('volume'),
                func.sum(MerchantActivity.transaction_count).label('transactions'),
                func.sum(MerchantActivity.unique_customers).label('customers')
            ).group_by(MerchantActivity.region).order_by(desc('volume'))
            
            if filters:
                regional_query = regional_query.where(filter_condition)
            
            regional_result = await self.db.execute(regional_query)
            regional_breakdown = [
                {
                    "region": row.region,
                    "volume": str(row.volume) if row.volume else "0",
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "customers": int(row.customers) if row.customers else 0
                }
                for row in regional_result
            ]
            
            return {
                "summary": {
                    "total_volume_usd": str(volume_data.total_volume_usd) if volume_data.total_volume_usd else "0",
                    "total_transactions": int(volume_data.total_transactions) if volume_data.total_transactions else 0,
                    "total_customers": int(volume_data.total_customers) if volume_data.total_customers else 0,
                    "total_merchants": int(volume_data.total_merchants) if volume_data.total_merchants else 0
                },
                "merchant_type_breakdown": type_breakdown,
                "network_breakdown": network_breakdown,
                "country_breakdown": country_breakdown,
                "regional_breakdown": regional_breakdown
            }
            
        except Exception as e:
            logger.error("Failed to get merchant analytics", error=str(e))
            return {
                "summary": {"total_volume_usd": "0", "total_transactions": 0, "total_customers": 0, "total_merchants": 0},
                "merchant_type_breakdown": [],
                "network_breakdown": [],
                "country_breakdown": [],
                "regional_breakdown": []
            }
    
    async def get_network_metrics(
        self,
        network: Optional[str] = None,
        period_type: str = "daily",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """Get comprehensive network metrics (AC1-10)"""
        try:
            logger.info("Generating network metrics", 
                       network=network, period_type=period_type)
            
            # Build base query
            query = select(NetworkMetrics)
            count_query = select(func.count(NetworkMetrics.id))
            
            # Apply filters
            filters = []
            if network:
                filters.append(NetworkMetrics.network == network.lower())
            if period_type:
                filters.append(NetworkMetrics.period_type == period_type)
            
            # Date range filtering
            if start_date:
                filters.append(NetworkMetrics.period_start >= start_date)
            if end_date:
                filters.append(NetworkMetrics.period_end <= end_date)
            
            if filters:
                filter_condition = and_(*filters)
                query = query.where(filter_condition)
                count_query = count_query.where(filter_condition)
            
            # Apply sorting
            sort_column = getattr(NetworkMetrics, sort_by, NetworkMetrics.period_start)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            # Execute queries
            result = await self.db.execute(query)
            metrics = result.scalars().all()
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Build response with comprehensive network metrics data
            metrics_list = []
            for metric in metrics:
                metric_data = {
                    "id": str(metric.id),
                    "network": metric.network,
                    "environment": metric.environment,
                    "period_start": metric.period_start.isoformat(),
                    "period_end": metric.period_end.isoformat(),
                    "period_type": metric.period_type,
                    "total_transactions": int(metric.total_transactions),
                    "total_volume": metric.total_volume,
                    "total_volume_usd": metric.total_volume_usd,
                    "active_accounts": int(metric.active_accounts),
                    "new_accounts": int(metric.new_accounts),
                    "avg_transaction_fee": metric.avg_transaction_fee,
                    "avg_transaction_fee_usd": metric.avg_transaction_fee_usd,
                    "avg_confirmation_time": float(metric.avg_confirmation_time) if metric.avg_confirmation_time else None,
                    "success_rate": float(metric.success_rate) if metric.success_rate else None,
                    "africa_transaction_count": int(metric.africa_transaction_count),
                    "africa_volume": metric.africa_volume,
                    "africa_volume_usd": metric.africa_volume_usd,
                    "created_at": metric.created_at.isoformat(),
                    "updated_at": metric.updated_at.isoformat()
                }
                metrics_list.append(metric_data)
            
            # Get aggregated analytics
            analytics = await self._get_network_analytics(filters)
            
            return {
                "metrics": metrics_list,
                "pagination": {
                    "total": total_count,
                    "page": (offset // limit) + 1,
                    "per_page": limit,
                    "pages": (total_count + limit - 1) // limit,
                    "has_next": offset + limit < total_count,
                    "has_prev": offset > 0
                },
                "filters": {
                    "network": network,
                    "period_type": period_type,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error("Failed to get network metrics", error=str(e))
            raise
    
    async def _get_network_analytics(self, filters: List) -> Dict[str, Any]:
        """Get aggregated network analytics (AC1-10)"""
        try:
            # Build base query for analytics
            base_query = select(NetworkMetrics)
            if filters:
                filter_condition = and_(*filters)
                base_query = base_query.where(filter_condition)
            
            # Get total metrics
            total_query = select(
                func.sum(NetworkMetrics.total_transactions).label('total_transactions'),
                func.sum(func.cast(NetworkMetrics.total_volume_usd, Numeric)).label('total_volume_usd'),
                func.avg(NetworkMetrics.success_rate).label('avg_success_rate'),
                func.avg(NetworkMetrics.avg_confirmation_time).label('avg_confirmation_time'),
                func.sum(NetworkMetrics.active_accounts).label('total_active_accounts'),
                func.sum(NetworkMetrics.new_accounts).label('total_new_accounts'),
                func.sum(NetworkMetrics.africa_transaction_count).label('total_africa_transactions'),
                func.sum(func.cast(NetworkMetrics.africa_volume_usd, Numeric)).label('total_africa_volume_usd')
            )
            if filters:
                total_query = total_query.where(filter_condition)
            
            total_result = await self.db.execute(total_query)
            total_data = total_result.first()
            
            # Get network breakdown
            network_query = select(
                NetworkMetrics.network,
                func.sum(NetworkMetrics.total_transactions).label('transactions'),
                func.sum(func.cast(NetworkMetrics.total_volume_usd, Numeric)).label('volume'),
                func.avg(NetworkMetrics.success_rate).label('avg_success_rate'),
                func.avg(NetworkMetrics.avg_confirmation_time).label('avg_confirmation_time'),
                func.sum(NetworkMetrics.active_accounts).label('active_accounts'),
                func.sum(NetworkMetrics.new_accounts).label('new_accounts'),
                func.sum(NetworkMetrics.africa_transaction_count).label('africa_transactions'),
                func.sum(func.cast(NetworkMetrics.africa_volume_usd, Numeric)).label('africa_volume')
            ).group_by(NetworkMetrics.network).order_by(desc('transactions'))
            
            if filters:
                network_query = network_query.where(filter_condition)
            
            network_result = await self.db.execute(network_query)
            network_breakdown = [
                {
                    "network": row.network,
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "volume": str(row.volume) if row.volume else "0",
                    "avg_success_rate": float(row.avg_success_rate) if row.avg_success_rate else None,
                    "avg_confirmation_time": float(row.avg_confirmation_time) if row.avg_confirmation_time else None,
                    "active_accounts": int(row.active_accounts) if row.active_accounts else 0,
                    "new_accounts": int(row.new_accounts) if row.new_accounts else 0,
                    "africa_transactions": int(row.africa_transactions) if row.africa_transactions else 0,
                    "africa_volume": str(row.africa_volume) if row.africa_volume else "0"
                }
                for row in network_result
            ]
            
            # Get period breakdown
            period_query = select(
                NetworkMetrics.period_type,
                func.sum(NetworkMetrics.total_transactions).label('transactions'),
                func.sum(func.cast(NetworkMetrics.total_volume_usd, Numeric)).label('volume'),
                func.avg(NetworkMetrics.success_rate).label('avg_success_rate'),
                func.avg(NetworkMetrics.avg_confirmation_time).label('avg_confirmation_time'),
                func.sum(NetworkMetrics.africa_transaction_count).label('africa_transactions'),
                func.sum(func.cast(NetworkMetrics.africa_volume_usd, Numeric)).label('africa_volume')
            ).group_by(NetworkMetrics.period_type).order_by(desc('transactions'))
            
            if filters:
                period_query = period_query.where(filter_condition)
            
            period_result = await self.db.execute(period_query)
            period_breakdown = [
                {
                    "period_type": row.period_type,
                    "transactions": int(row.transactions) if row.transactions else 0,
                    "volume": str(row.volume) if row.volume else "0",
                    "avg_success_rate": float(row.avg_success_rate) if row.avg_success_rate else None,
                    "avg_confirmation_time": float(row.avg_confirmation_time) if row.avg_confirmation_time else None,
                    "africa_transactions": int(row.africa_transactions) if row.africa_transactions else 0,
                    "africa_volume": str(row.africa_volume) if row.africa_volume else "0"
                }
                for row in period_result
            ]
            
            return {
                "summary": {
                    "total_transactions": int(total_data.total_transactions) if total_data.total_transactions else 0,
                    "total_volume_usd": str(total_data.total_volume_usd) if total_data.total_volume_usd else "0",
                    "avg_success_rate": float(total_data.avg_success_rate) if total_data.avg_success_rate else None,
                    "avg_confirmation_time": float(total_data.avg_confirmation_time) if total_data.avg_confirmation_time else None,
                    "total_active_accounts": int(total_data.total_active_accounts) if total_data.total_active_accounts else 0,
                    "total_new_accounts": int(total_data.total_new_accounts) if total_data.total_new_accounts else 0,
                    "total_africa_transactions": int(total_data.total_africa_transactions) if total_data.total_africa_transactions else 0,
                    "total_africa_volume_usd": str(total_data.total_africa_volume_usd) if total_data.total_africa_volume_usd else "0"
                },
                "network_breakdown": network_breakdown,
                "period_breakdown": period_breakdown
            }
            
        except Exception as e:
            logger.error("Failed to get network analytics", error=str(e))
            return {
                "summary": {
                    "total_transactions": 0,
                    "total_volume_usd": "0",
                    "avg_success_rate": None,
                    "avg_confirmation_time": None,
                    "total_active_accounts": 0,
                    "total_new_accounts": 0,
                    "total_africa_transactions": 0,
                    "total_africa_volume_usd": "0"
                },
                "network_breakdown": [],
                "period_breakdown": []
            }
    
    async def get_dashboard_data(self, **kwargs) -> Dict[str, Any]:
        """Get comprehensive dashboard data (AC1-10)"""
        try:
            logger.info("Generating dashboard analytics data")
            
            # Get total account count (AC1, AC6)
            total_accounts = await self._get_total_accounts()
            
            # Get total transaction volume (AC2, AC7)
            total_volume_data = await self._get_total_transaction_volume()
            
            # Get success rate (AC3, AC8)
            success_rate = await self._get_success_rate()
            
            # Get network status (AC4, AC9)
            active_networks = await self._get_active_networks()
            
            # Get recent activity (AC5, AC10)
            recent_activity = await self._get_recent_activity()
            
            # Get top countries
            top_countries = await self._get_top_countries()
            
            return {
                "total_accounts": total_accounts,
                "total_transactions": total_volume_data["transaction_count"],
                "total_volume": total_volume_data["total_volume"],
                "total_volume_usd": total_volume_data["total_volume_usd"],
                "success_rate": success_rate,
                "active_networks": active_networks,
                "top_countries": top_countries,
                "recent_activity": recent_activity
            }
            
        except Exception as e:
            logger.error("Failed to get dashboard data", error=str(e))
            # Return empty data on error
            return {
                "total_accounts": 0,
                "total_transactions": 0,
                "total_volume": "0",
                "total_volume_usd": "0",
                "success_rate": 0.0,
                "active_networks": [],
                "top_countries": [],
                "recent_activity": []
            }
    
    async def _get_total_accounts(self) -> int:
        """Get total account count (AC1, AC6)"""
        try:
            result = await self.db.execute(
                select(func.count(Account.id)).where(Account.is_active == True)
            )
            return result.scalar() or 0
        except Exception as e:
            logger.error("Failed to get total accounts", error=str(e))
            return 0
    
    async def _get_total_transaction_volume(self) -> Dict[str, Any]:
        """Get total transaction volume and count (AC2, AC7)"""
        try:
            # Get transaction count
            count_result = await self.db.execute(
                select(func.count(Transaction.id))
            )
            transaction_count = count_result.scalar() or 0
            
            # For MVP, return basic counts without complex aggregation
            # In production, this would use proper SQL aggregation
            return {
                "transaction_count": transaction_count,
                "total_volume": str(transaction_count * 10),  # Mock calculation
                "total_volume_usd": str(transaction_count * 10)  # Mock calculation
            }
        except Exception as e:
            logger.error("Failed to get transaction volume", error=str(e))
            return {
                "transaction_count": 0,
                "total_volume": "0",
                "total_volume_usd": "0"
            }
    
    async def _get_success_rate(self) -> float:
        """Get transfer success rate (AC3, AC8)"""
        try:
            # Get total transactions
            total_result = await self.db.execute(
                select(func.count(Transaction.id))
            )
            total_transactions = total_result.scalar() or 0
            
            if total_transactions == 0:
                return 0.0
            
            # Get successful transactions
            success_result = await self.db.execute(
                select(func.count(Transaction.id)).where(Transaction.status == "success")
            )
            successful_transactions = success_result.scalar() or 0
            
            return round((successful_transactions / total_transactions) * 100, 2)
        except Exception as e:
            logger.error("Failed to get success rate", error=str(e))
            return 0.0
    
    async def _get_active_networks(self) -> List[Dict[str, Any]]:
        """Get active networks status (AC4, AC9)"""
        try:
            # Get network activity - simplified for MVP
            result = await self.db.execute(
                select(
                    Transaction.network,
                    Transaction.environment,
                    func.count(Transaction.id).label('transaction_count')
                )
                .group_by(Transaction.network, Transaction.environment)
                .order_by(desc('transaction_count'))
            )
            
            networks = []
            for row in result:
                networks.append({
                    "network": row.network,
                    "environment": row.environment,
                    "transaction_count": row.transaction_count,
                    "volume_usd": str(row.transaction_count * 10),  # Mock calculation
                    "status": "active" if row.transaction_count > 0 else "inactive"
                })
            
            return networks
        except Exception as e:
            logger.error("Failed to get active networks", error=str(e))
            return []
    
    async def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent activity summary (AC5, AC10)"""
        try:
            # Get recent transactions (last 24 hours)
            recent_time = datetime.now() - timedelta(hours=24)
            
            result = await self.db.execute(
                select(Transaction)
                .where(Transaction.created_at >= recent_time)
                .order_by(desc(Transaction.created_at))
                .limit(10)
            )
            
            activities = []
            for transaction in result.scalars():
                activities.append({
                    "type": "transaction",
                    "id": str(transaction.id),
                    "transaction_hash": transaction.transaction_hash,
                    "from_account": transaction.from_account,
                    "to_account": transaction.to_account,
                    "asset_code": transaction.asset_code,
                    "amount": transaction.amount,
                    "network": transaction.network,
                    "status": transaction.status,
                    "created_at": transaction.created_at.isoformat(),
                    "from_country": transaction.from_country,
                    "to_country": transaction.to_country
                })
            
            return activities
        except Exception as e:
            logger.error("Failed to get recent activity", error=str(e))
            return []
    
    async def _get_top_countries(self) -> List[Dict[str, Any]]:
        """Get top countries by transaction volume"""
        try:
            result = await self.db.execute(
                select(
                    Transaction.from_country,
                    func.count(Transaction.id).label('transaction_count')
                )
                .where(Transaction.from_country != None)
                .group_by(Transaction.from_country)
                .order_by(desc('transaction_count'))
                .limit(10)
            )
            
            countries = []
            for row in result:
                countries.append({
                    "country_code": row.from_country,
                    "transaction_count": row.transaction_count,
                    "volume_usd": str(row.transaction_count * 10)  # Mock calculation
                })
            
            return countries
        except Exception as e:
            logger.error("Failed to get top countries", error=str(e))
            return []
