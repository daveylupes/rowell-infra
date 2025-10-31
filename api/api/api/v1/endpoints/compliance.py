"""
Compliance and KYC endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, Field
import structlog

from api.core.database import get_db
from api.services.compliance_service import ComplianceService

logger = structlog.get_logger()
router = APIRouter()


# Pydantic models for request/response
class KYCVerificationRequest(BaseModel):
    """Request model for KYC verification"""
    account_id: str = Field(..., description="Account ID to verify")
    network: str = Field(..., description="Network: 'stellar' or 'hedera'")
    verification_type: str = Field(..., description="Verification type: 'individual', 'business', 'ngo'")
    
    # Personal information
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    date_of_birth: Optional[str] = Field(None, description="Date of birth (YYYY-MM-DD)")
    nationality: Optional[str] = Field(None, description="Nationality (ISO country code)")
    
    # Document information
    document_type: Optional[str] = Field(None, description="Document type: 'passport', 'national_id', 'drivers_license', 'bvn'")
    document_number: Optional[str] = Field(None, description="Document number")
    document_country: Optional[str] = Field(None, description="Document country (ISO country code)")
    
    # Africa-specific fields
    bvn: Optional[str] = Field(None, description="Nigeria Bank Verification Number")
    nin: Optional[str] = Field(None, description="Nigeria National Identification Number")
    sa_id_number: Optional[str] = Field(None, description="South Africa ID Number")
    ghana_card: Optional[str] = Field(None, description="Ghana Card Number")


class KYCVerificationResponse(BaseModel):
    """Response model for KYC verification"""
    id: str
    verification_id: str
    account_id: str
    network: str
    verification_type: str
    verification_status: str
    provider: str
    verification_score: Optional[float]
    risk_level: Optional[str]
    verification_notes: Optional[str]
    created_at: str
    updated_at: str
    verified_at: Optional[str]
    expires_at: Optional[str]


class ComplianceFlagRequest(BaseModel):
    """Request model for flagging transactions/accounts"""
    entity_type: str = Field(..., description="Entity type: 'account' or 'transaction'")
    entity_id: str = Field(..., description="Account ID or transaction hash")
    network: str = Field(..., description="Network: 'stellar' or 'hedera'")
    flag_type: str = Field(..., description="Flag type: 'aml', 'kyc', 'sanctions', 'risk'")
    flag_severity: str = Field(..., description="Flag severity: 'low', 'medium', 'high', 'critical'")
    flag_reason: str = Field(..., description="Reason for flagging")
    flag_data: Optional[dict] = Field(None, description="Additional flag data")
    country_code: Optional[str] = Field(None, description="Country code")
    region: Optional[str] = Field(None, description="Region")


class ComplianceFlagResponse(BaseModel):
    """Response model for compliance flags"""
    id: str
    entity_type: str
    entity_id: str
    network: str
    flag_type: str
    flag_severity: str
    flag_status: str
    flag_reason: str
    risk_score: Optional[float]
    country_code: Optional[str]
    region: Optional[str]
    resolved_by: Optional[str]
    resolution_notes: Optional[str]
    created_at: str
    updated_at: str
    resolved_at: Optional[str]


class ComplianceReportResponse(BaseModel):
    """Response model for compliance reports"""
    id: str
    report_type: str
    report_period: str
    country_code: Optional[str]
    region: Optional[str]
    total_verifications: int
    successful_verifications: int
    failed_verifications: int
    pending_verifications: int
    total_flags: int
    active_flags: int
    resolved_flags: int
    false_positive_flags: int
    avg_risk_score: Optional[float]
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    period_start: str
    period_end: str
    summary: Optional[str]
    created_at: str


@router.post("/verify-id", response_model=KYCVerificationResponse, status_code=status.HTTP_201_CREATED)
async def verify_id(
    request: KYCVerificationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Initiate KYC verification for an account"""
    try:
        logger.info(
            "Initiating KYC verification",
            account_id=request.account_id,
            network=request.network,
            verification_type=request.verification_type
        )
        
        compliance_service = ComplianceService(db)
        
        # Prepare verification data
        verification_data = {
            "account_id": request.account_id,
            "network": request.network,
            "verification_type": request.verification_type,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "date_of_birth": request.date_of_birth,
            "nationality": request.nationality,
            "document_type": request.document_type,
            "document_number": request.document_number,
            "document_country": request.document_country,
            "bvn": request.bvn,
            "nin": request.nin,
            "sa_id_number": request.sa_id_number,
            "ghana_card": request.ghana_card
        }
        
        # Initiate KYC verification
        result = await compliance_service.verify_id(verification_data)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        logger.info("KYC verification initiated", verification_id=result["verification_id"])
        
        return {
            "verification_id": result["verification_id"],
            "verification_status": result["verification_status"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "verification_notes": result["verification_notes"],
            "expires_at": result["expires_at"]
        }
        
    except Exception as e:
        logger.error("Failed to initiate KYC verification", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate KYC verification: {str(e)}"
        )


@router.get("/verify-id/{verification_id}", response_model=KYCVerificationResponse)
async def get_kyc_verification(
    verification_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get KYC verification status"""
    try:
        compliance_service = ComplianceService(db)
        result = await compliance_service.get_verification_status(verification_id)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KYC verification not found"
            )
        
        return {
            "verification_id": result["verification_id"],
            "verification_status": result["verification_status"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "verification_notes": result["verification_notes"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
            "verified_at": result["verified_at"],
            "expires_at": result["expires_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get KYC verification", verification_id=verification_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get KYC verification: {str(e)}"
        )


@router.get("/verifications")
async def list_verifications(
    account_id: Optional[str] = None,
    verification_status: Optional[str] = None,
    verification_type: Optional[str] = None,
    network: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List KYC verifications with filtering and pagination"""
    try:
        compliance_service = ComplianceService(db)
        result = await compliance_service.list_verifications(
            account_id=account_id,
            verification_status=verification_status,
            verification_type=verification_type,
            network=network,
            limit=limit,
            offset=offset
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list verifications", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list verifications: {str(e)}"
        )


@router.post("/flag-transaction", response_model=ComplianceFlagResponse, status_code=status.HTTP_201_CREATED)
async def flag_transaction(
    request: ComplianceFlagRequest,
    db: AsyncSession = Depends(get_db)
):
    """Flag a transaction or account for compliance review"""
    try:
        logger.info(
            "Flagging entity for compliance",
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            flag_type=request.flag_type,
            flag_severity=request.flag_severity
        )
        
        compliance_service = ComplianceService(db)
        
        # Prepare flag data
        flag_data = {
            "entity_type": request.entity_type,
            "entity_id": request.entity_id,
            "network": request.network,
            "flag_type": request.flag_type,
            "flag_severity": request.flag_severity,
            "flag_reason": request.flag_reason,
            "country_code": request.country_code,
            "region": request.region
        }
        
        # Create compliance flag
        result = await compliance_service.flag_transaction(flag_data)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        logger.info("Compliance flag created", flag_id=result["flag_id"])
        
        return {
            "flag_id": result["flag_id"],
            "flag_status": result["flag_status"],
            "created_at": result["created_at"]
        }
        
    except Exception as e:
        logger.error("Failed to create compliance flag", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create compliance flag: {str(e)}"
        )


@router.get("/flags")
async def list_compliance_flags(
    entity_type: Optional[str] = None,
    flag_type: Optional[str] = None,
    flag_severity: Optional[str] = None,
    flag_status: Optional[str] = None,
    network: Optional[str] = None,
    country_code: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """List compliance flags with optional filtering, pagination, and sorting"""
    try:
        # Validate parameters
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 1
        if offset < 0:
            offset = 0
        
        if sort_by not in ["created_at", "updated_at", "risk_score", "flag_severity"]:
            sort_by = "created_at"
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"
        
        compliance_service = ComplianceService(db)
        result = await compliance_service.list_compliance_flags(
            entity_type=entity_type,
            flag_type=flag_type,
            flag_severity=flag_severity,
            flag_status=flag_status,
            network=network,
            country_code=country_code,
            region=region,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list compliance flags", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list compliance flags: {str(e)}"
        )


@router.get("/flags/{flag_id}")
async def get_flag_details(
    flag_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific compliance flag"""
    try:
        compliance_service = ComplianceService(db)
        result = await compliance_service.get_flag_details(flag_id)
        
        if not result["success"]:
            if "not found" in result["error"].lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result["error"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get flag details", flag_id=flag_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flag details: {str(e)}"
        )


@router.patch("/flags/{flag_id}/status")
async def update_flag_status(
    flag_id: str,
    new_status: str,
    resolved_by: Optional[str] = None,
    resolution_notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update the status of a compliance flag"""
    try:
        # Validate status
        valid_statuses = ["active", "resolved", "closed", "escalated"]
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        compliance_service = ComplianceService(db)
        result = await compliance_service.update_flag_status(
            flag_id=flag_id,
            new_status=new_status,
            resolved_by=resolved_by,
            resolution_notes=resolution_notes
        )
        
        if not result["success"]:
            if "not found" in result["error"].lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result["error"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update flag status", flag_id=flag_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update flag status: {str(e)}"
        )


@router.get("/flags/analytics")
async def get_flag_analytics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    network: Optional[str] = None,
    country_code: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get analytics and summary statistics for compliance flags"""
    try:
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        compliance_service = ComplianceService(db)
        result = await compliance_service.get_flag_analytics(
            start_date=start_dt,
            end_date=end_dt,
            network=network,
            country_code=country_code
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get flag analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flag analytics: {str(e)}"
        )


@router.patch("/flags/{flag_id}/resolve")
async def resolve_compliance_flag(
    flag_id: str,
    resolved_by: str,
    resolution_notes: str,
    resolution_data: Optional[dict] = None,
    db: AsyncSession = Depends(get_db)
):
    """Resolve a compliance flag"""
    try:
        compliance_service = ComplianceService(db)
        result = await compliance_service.resolve_compliance_flag(
            flag_id=flag_id,
            resolved_by=resolved_by,
            resolution_notes=resolution_notes,
            resolution_data=resolution_data
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compliance flag not found"
            )
        
        return {"message": "Compliance flag resolved successfully", "flag_id": flag_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to resolve compliance flag", flag_id=flag_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resolve compliance flag: {str(e)}"
        )


@router.get("/reports", response_model=List[ComplianceReportResponse])
async def get_compliance_reports(
    report_type: Optional[str] = None,
    report_period: Optional[str] = None,
    country_code: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get compliance reports"""
    try:
        compliance_service = ComplianceService(db)
        reports = await compliance_service.get_compliance_reports(
            report_type=report_type,
            report_period=report_period,
            country_code=country_code,
            region=region,
            limit=limit,
            offset=offset
        )
        
        return [
            ComplianceReportResponse(
                id=str(report.id),
                report_type=report.report_type,
                report_period=report.report_period,
                country_code=report.country_code,
                region=report.region,
                total_verifications=int(report.total_verifications),
                successful_verifications=int(report.successful_verifications),
                failed_verifications=int(report.failed_verifications),
                pending_verifications=int(report.pending_verifications),
                total_flags=int(report.total_flags),
                active_flags=int(report.active_flags),
                resolved_flags=int(report.resolved_flags),
                false_positive_flags=int(report.false_positive_flags),
                avg_risk_score=float(report.avg_risk_score) if report.avg_risk_score else None,
                high_risk_count=int(report.high_risk_count),
                medium_risk_count=int(report.medium_risk_count),
                low_risk_count=int(report.low_risk_count),
                period_start=report.period_start.isoformat(),
                period_end=report.period_end.isoformat(),
                summary=report.summary,
                created_at=report.created_at.isoformat()
            )
            for report in reports
        ]
        
    except Exception as e:
        logger.error("Failed to get compliance reports", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get compliance reports: {str(e)}"
        )
