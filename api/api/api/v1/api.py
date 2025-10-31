"""
Main API router for Rowell Infra v1
"""

from fastapi import APIRouter
from api.api.v1.endpoints import accounts, transactions, analytics, compliance, transfers, developers, sandbox, auth
# from api.api.v1.endpoints import documentation  # Temporarily disabled due to import issues

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(developers.router, prefix="/developers", tags=["developers"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(transfers.router, prefix="/transfers", tags=["transfers"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
# api_router.include_router(documentation.router, prefix="/docs", tags=["documentation"])  # Temporarily disabled
api_router.include_router(sandbox.router, prefix="/sandbox", tags=["sandbox"])
