"""
Compliance service for handling compliance operations
"""

import re
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from api.models.compliance import KYCVerification, ComplianceFlag
from api.models.account import Account


class ComplianceService:
    """Service for compliance and KYC operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def verify_id(self, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate KYC verification with African ID support"""
        try:
            # Generate unique verification ID
            verification_id = f"KYC_{uuid.uuid4().hex[:12].upper()}"
            
            # Validate ID formats based on type
            validation_result = await self._validate_id_formats(verification_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "Invalid ID format",
                    "details": validation_result["errors"]
                }
            
            # Check against sanctions lists
            sanctions_result = await self._check_sanctions_lists(verification_data)
            
            # Calculate risk score
            risk_score = await self._calculate_risk_score(verification_data, sanctions_result)
            
            # Determine verification status
            verification_status = self._determine_verification_status(risk_score, validation_result)
            
            # Create KYC verification record
            kyc_record = KYCVerification(
                id=str(uuid.uuid4()),
                account_id=verification_data["account_id"],
                network=verification_data["network"],
                verification_id=verification_id,
                verification_type=verification_data["verification_type"],
                verification_status=verification_status,
                first_name=verification_data.get("first_name"),
                last_name=verification_data.get("last_name"),
                date_of_birth=datetime.fromisoformat(verification_data["date_of_birth"]) if verification_data.get("date_of_birth") else None,
                nationality=verification_data.get("nationality"),
                document_type=verification_data.get("document_type"),
                document_number=verification_data.get("document_number"),
                document_country=verification_data.get("document_country"),
                bvn=verification_data.get("bvn"),
                nin=verification_data.get("nin"),
                sa_id_number=verification_data.get("sa_id_number"),
                ghana_card=verification_data.get("ghana_card"),
                provider="mock",  # For MVP, using mock provider
                verification_score=risk_score,
                risk_level=self._get_risk_level(risk_score),
                verification_notes=f"ID validation: {validation_result['status']}, Sanctions check: {sanctions_result['status']}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                verified_at=datetime.now() if verification_status == "verified" else None,
                expires_at=datetime.now() + timedelta(days=365) if verification_status == "verified" else None
            )
            
            self.db.add(kyc_record)
            await self.db.commit()
            await self.db.refresh(kyc_record)
            
            return {
                "success": True,
                "verification_id": verification_id,
                "verification_status": verification_status,
                "risk_score": risk_score,
                "risk_level": self._get_risk_level(risk_score),
                "verification_notes": kyc_record.verification_notes,
                "expires_at": kyc_record.expires_at.isoformat() if kyc_record.expires_at else None
            }
            
        except Exception as e:
            await self.db.rollback()
            return {
                "success": False,
                "error": f"KYC verification failed: {str(e)}"
            }
    
    async def _validate_id_formats(self, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate ID number formats for African ID types"""
        errors = []
        validation_results = {}
        
        # BVN validation (Nigeria)
        if verification_data.get("bvn"):
            bvn = verification_data["bvn"]
            if not re.match(r'^\d{11}$', bvn):
                errors.append("BVN must be exactly 11 digits")
            else:
                validation_results["bvn"] = "valid"
        
        # NIN validation (Nigeria)
        if verification_data.get("nin"):
            nin = verification_data["nin"]
            if not re.match(r'^\d{11}$', nin):
                errors.append("NIN must be exactly 11 digits")
            else:
                validation_results["nin"] = "valid"
        
        # SA ID validation (South Africa)
        if verification_data.get("sa_id_number"):
            sa_id = verification_data["sa_id_number"]
            if not re.match(r'^\d{13}$', sa_id):
                errors.append("SA ID must be exactly 13 digits")
            else:
                # Basic SA ID validation (check digit)
                if self._validate_sa_id_checksum(sa_id):
                    validation_results["sa_id_number"] = "valid"
                else:
                    errors.append("SA ID checksum validation failed")
        
        # Ghana Card validation
        if verification_data.get("ghana_card"):
            ghana_card = verification_data["ghana_card"]
            if not re.match(r'^GHA-\d{9}-\d$', ghana_card):
                errors.append("Ghana Card must be in format GHA-XXXXXXXXX-X")
            else:
                validation_results["ghana_card"] = "valid"
        
        # Generic document number validation
        if verification_data.get("document_number") and not any([
            verification_data.get("bvn"),
            verification_data.get("nin"),
            verification_data.get("sa_id_number"),
            verification_data.get("ghana_card")
        ]):
            doc_number = verification_data["document_number"]
            if len(doc_number) < 5 or len(doc_number) > 20:
                errors.append("Document number must be between 5 and 20 characters")
            else:
                validation_results["document_number"] = "valid"
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "status": "valid" if len(errors) == 0 else "invalid",
            "validation_results": validation_results
        }
    
    def _validate_sa_id_checksum(self, sa_id: str) -> bool:
        """Validate South African ID checksum"""
        if len(sa_id) != 13:
            return False
        
        # Basic checksum validation (simplified for MVP)
        digits = [int(d) for d in sa_id]
        odd_sum = sum(digits[i] for i in range(0, 12, 2))
        even_sum = sum(digits[i] for i in range(1, 12, 2))
        total = odd_sum + even_sum * 2
        
        # For MVP, accept any 13-digit number
        return True
    
    async def _check_sanctions_lists(self, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check against sanctions lists (mock implementation)"""
        # Mock sanctions check - in production, integrate with real sanctions databases
        sanctions_hit = False
        sanctions_details = []
        
        # Mock check against common names (for demo purposes)
        first_name = verification_data.get("first_name", "").lower()
        last_name = verification_data.get("last_name", "").lower()
        
        # Mock sanctions list
        mock_sanctions = ["john", "jane", "test"]
        
        if first_name in mock_sanctions or last_name in mock_sanctions:
            sanctions_hit = True
            sanctions_details.append(f"Name match found in sanctions list")
        
        return {
            "hit": sanctions_hit,
            "status": "clear" if not sanctions_hit else "flagged",
            "details": sanctions_details
        }
    
    async def _calculate_risk_score(self, verification_data: Dict[str, Any], sanctions_result: Dict[str, Any]) -> float:
        """Calculate risk score based on multiple factors"""
        risk_score = 0.0
        
        # Base score
        risk_score += 20.0
        
        # Document type risk
        doc_type = verification_data.get("document_type", "")
        if doc_type == "passport":
            risk_score += 10.0
        elif doc_type == "national_id":
            risk_score += 5.0
        elif doc_type == "bvn":
            risk_score += 2.0  # BVN is considered low risk
        
        # Country risk (simplified)
        country = verification_data.get("document_country", "")
        high_risk_countries = ["XX", "YY"]  # Mock high-risk countries
        if country in high_risk_countries:
            risk_score += 15.0
        
        # Sanctions check
        if sanctions_result["hit"]:
            risk_score += 50.0
        
        # Age risk (if date of birth provided)
        if verification_data.get("date_of_birth"):
            try:
                dob = datetime.fromisoformat(verification_data["date_of_birth"])
                age = (datetime.now() - dob).days / 365.25
                if age < 18:
                    risk_score += 20.0
                elif age > 80:
                    risk_score += 10.0
            except:
                risk_score += 5.0
        
        # Ensure score is between 0 and 100
        return min(100.0, max(0.0, risk_score))
    
    def _determine_verification_status(self, risk_score: float, validation_result: Dict[str, Any]) -> str:
        """Determine verification status based on risk score and validation"""
        if not validation_result["valid"]:
            return "rejected"
        
        if risk_score >= 70:
            return "rejected"
        elif risk_score >= 40:
            return "pending"  # Manual review required
        else:
            return "verified"
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level based on score"""
        if risk_score >= 70:
            return "high"
        elif risk_score >= 40:
            return "medium"
        else:
            return "low"
    
    async def get_verification_status(self, verification_id: str) -> Dict[str, Any]:
        """Get KYC verification status"""
        try:
            result = await self.db.execute(
                select(KYCVerification).where(KYCVerification.verification_id == verification_id)
            )
            kyc_record = result.scalar_one_or_none()
            
            if not kyc_record:
                return {
                    "success": False,
                    "error": "Verification not found"
                }
            
            return {
                "success": True,
                "verification_id": kyc_record.verification_id,
                "verification_status": kyc_record.verification_status,
                "risk_score": float(kyc_record.verification_score) if kyc_record.verification_score else None,
                "risk_level": kyc_record.risk_level,
                "verification_notes": kyc_record.verification_notes,
                "created_at": kyc_record.created_at.isoformat(),
                "updated_at": kyc_record.updated_at.isoformat(),
                "verified_at": kyc_record.verified_at.isoformat() if kyc_record.verified_at else None,
                "expires_at": kyc_record.expires_at.isoformat() if kyc_record.expires_at else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get verification status: {str(e)}"
            }
    
    async def list_verifications(self, account_id: Optional[str] = None, 
                               verification_status: Optional[str] = None,
                               verification_type: Optional[str] = None,
                               network: Optional[str] = None,
                               limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List KYC verifications with filtering and pagination"""
        try:
            # Build query
            query = select(KYCVerification)
            conditions = []
            
            if account_id:
                conditions.append(KYCVerification.account_id == account_id)
            if verification_status:
                conditions.append(KYCVerification.verification_status == verification_status)
            if verification_type:
                conditions.append(KYCVerification.verification_type == verification_type)
            if network:
                conditions.append(KYCVerification.network == network)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Get total count
            count_query = select(func.count(KYCVerification.id))
            if conditions:
                count_query = count_query.where(and_(*conditions))
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Get paginated results
            query = query.order_by(KYCVerification.created_at.desc()).limit(limit).offset(offset)
            result = await self.db.execute(query)
            verifications = result.scalars().all()
            
            # Format results
            verification_list = []
            for verification in verifications:
                verification_list.append({
                    "id": verification.id,
                    "verification_id": verification.verification_id,
                    "account_id": verification.account_id,
                    "network": verification.network,
                    "verification_type": verification.verification_type,
                    "verification_status": verification.verification_status,
                    "risk_score": float(verification.verification_score) if verification.verification_score else None,
                    "risk_level": verification.risk_level,
                    "created_at": verification.created_at.isoformat(),
                    "updated_at": verification.updated_at.isoformat(),
                    "verified_at": verification.verified_at.isoformat() if verification.verified_at else None,
                    "expires_at": verification.expires_at.isoformat() if verification.expires_at else None
                })
            
            return {
                "success": True,
                "verifications": verification_list,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list verifications: {str(e)}"
            }
    
    async def flag_transaction(self, flag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Flag a transaction for compliance review"""
        try:
            flag_id = str(uuid.uuid4())
            
            # Create compliance flag
            flag = ComplianceFlag(
                id=flag_id,
                entity_type=flag_data["entity_type"],
                entity_id=flag_data["entity_id"],
                network=flag_data["network"],
                flag_type=flag_data["flag_type"],
                flag_severity=flag_data["flag_severity"],
                flag_status="active",
                flag_reason=flag_data["flag_reason"],
                risk_score=flag_data.get("risk_score"),
                country_code=flag_data.get("country_code"),
                region=flag_data.get("region"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.db.add(flag)
            await self.db.commit()
            await self.db.refresh(flag)
            
            return {
                "success": True,
                "flag_id": flag_id,
                "flag_status": "active",
                "created_at": flag.created_at.isoformat()
            }
            
        except Exception as e:
            await self.db.rollback()
            return {
                "success": False,
                "error": f"Failed to flag transaction: {str(e)}"
            }
    
    async def list_compliance_flags(self, 
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
                                   sort_order: str = "desc") -> Dict[str, Any]:
        """List compliance flags with filtering, pagination, and sorting"""
        try:
            # Build query
            query = select(ComplianceFlag)
            conditions = []
            
            if entity_type:
                conditions.append(ComplianceFlag.entity_type == entity_type)
            if flag_type:
                conditions.append(ComplianceFlag.flag_type == flag_type)
            if flag_severity:
                conditions.append(ComplianceFlag.flag_severity == flag_severity)
            if flag_status:
                conditions.append(ComplianceFlag.flag_status == flag_status)
            if network:
                conditions.append(ComplianceFlag.network == network)
            if country_code:
                conditions.append(ComplianceFlag.country_code == country_code)
            if region:
                conditions.append(ComplianceFlag.region == region)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Get total count
            count_query = select(func.count(ComplianceFlag.id))
            if conditions:
                count_query = count_query.where(and_(*conditions))
            
            count_result = await self.db.execute(count_query)
            total_count = count_result.scalar()
            
            # Apply sorting
            if sort_by == "created_at":
                sort_column = ComplianceFlag.created_at
            elif sort_by == "updated_at":
                sort_column = ComplianceFlag.updated_at
            elif sort_by == "risk_score":
                sort_column = ComplianceFlag.risk_score
            elif sort_by == "flag_severity":
                sort_column = ComplianceFlag.flag_severity
            else:
                sort_column = ComplianceFlag.created_at
            
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
            
            # Get paginated results
            query = query.limit(limit).offset(offset)
            result = await self.db.execute(query)
            flags = result.scalars().all()
            
            # Format results
            flag_list = []
            for flag in flags:
                flag_list.append({
                    "id": flag.id,
                    "entity_type": flag.entity_type,
                    "entity_id": flag.entity_id,
                    "network": flag.network,
                    "flag_type": flag.flag_type,
                    "flag_severity": flag.flag_severity,
                    "flag_status": flag.flag_status,
                    "flag_reason": flag.flag_reason,
                    "risk_score": float(flag.risk_score) if flag.risk_score else None,
                    "country_code": flag.country_code,
                    "region": flag.region,
                    "resolved_by": flag.resolved_by,
                    "resolution_notes": flag.resolution_notes,
                    "created_at": flag.created_at.isoformat(),
                    "updated_at": flag.updated_at.isoformat(),
                    "resolved_at": flag.resolved_at.isoformat() if flag.resolved_at else None
                })
            
            return {
                "success": True,
                "flags": flag_list,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "filters": {
                    "entity_type": entity_type,
                    "flag_type": flag_type,
                    "flag_severity": flag_severity,
                    "flag_status": flag_status,
                    "network": network,
                    "country_code": country_code,
                    "region": region
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list compliance flags: {str(e)}"
            }
    
    async def get_flag_details(self, flag_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific compliance flag"""
        try:
            result = await self.db.execute(
                select(ComplianceFlag).where(ComplianceFlag.id == flag_id)
            )
            flag = result.scalar_one_or_none()
            
            if not flag:
                return {
                    "success": False,
                    "error": "Flag not found"
                }
            
            # Get flag history/audit trail
            history = await self._get_flag_history(flag_id)
            
            # Get related entity information
            entity_info = await self._get_entity_info(flag.entity_type, flag.entity_id)
            
            return {
                "success": True,
                "flag": {
                    "id": flag.id,
                    "entity_type": flag.entity_type,
                    "entity_id": flag.entity_id,
                    "network": flag.network,
                    "flag_type": flag.flag_type,
                    "flag_severity": flag.flag_severity,
                    "flag_status": flag.flag_status,
                    "flag_reason": flag.flag_reason,
                    "risk_score": float(flag.risk_score) if flag.risk_score else None,
                    "country_code": flag.country_code,
                    "region": flag.region,
                    "resolved_by": flag.resolved_by,
                    "resolution_notes": flag.resolution_notes,
                    "created_at": flag.created_at.isoformat(),
                    "updated_at": flag.updated_at.isoformat(),
                    "resolved_at": flag.resolved_at.isoformat() if flag.resolved_at else None
                },
                "history": history,
                "entity_info": entity_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get flag details: {str(e)}"
            }
    
    async def update_flag_status(self, flag_id: str, 
                               new_status: str, 
                               resolved_by: Optional[str] = None,
                               resolution_notes: Optional[str] = None) -> Dict[str, Any]:
        """Update the status of a compliance flag"""
        try:
            result = await self.db.execute(
                select(ComplianceFlag).where(ComplianceFlag.id == flag_id)
            )
            flag = result.scalar_one_or_none()
            
            if not flag:
                return {
                    "success": False,
                    "error": "Flag not found"
                }
            
            # Update flag status
            flag.flag_status = new_status
            flag.updated_at = datetime.now()
            
            if new_status in ["resolved", "closed"]:
                flag.resolved_by = resolved_by
                flag.resolution_notes = resolution_notes
                flag.resolved_at = datetime.now()
            
            await self.db.commit()
            await self.db.refresh(flag)
            
            return {
                "success": True,
                "flag_id": flag_id,
                "new_status": new_status,
                "updated_at": flag.updated_at.isoformat(),
                "resolved_at": flag.resolved_at.isoformat() if flag.resolved_at else None
            }
            
        except Exception as e:
            await self.db.rollback()
            return {
                "success": False,
                "error": f"Failed to update flag status: {str(e)}"
            }
    
    async def get_flag_analytics(self, 
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None,
                               network: Optional[str] = None,
                               country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get analytics and summary statistics for compliance flags"""
        try:
            # Build base query
            query = select(ComplianceFlag)
            conditions = []
            
            if start_date:
                conditions.append(ComplianceFlag.created_at >= start_date)
            if end_date:
                conditions.append(ComplianceFlag.created_at <= end_date)
            if network:
                conditions.append(ComplianceFlag.network == network)
            if country_code:
                conditions.append(ComplianceFlag.country_code == country_code)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Get all flags for analysis
            result = await self.db.execute(query)
            flags = result.scalars().all()
            
            # Calculate analytics
            total_flags = len(flags)
            active_flags = len([f for f in flags if f.flag_status == "active"])
            resolved_flags = len([f for f in flags if f.flag_status == "resolved"])
            closed_flags = len([f for f in flags if f.flag_status == "closed"])
            
            # Severity breakdown
            severity_breakdown = {}
            for severity in ["low", "medium", "high", "critical"]:
                severity_breakdown[severity] = len([f for f in flags if f.flag_severity == severity])
            
            # Type breakdown
            type_breakdown = {}
            for flag_type in ["aml", "kyc", "sanctions", "risk"]:
                type_breakdown[flag_type] = len([f for f in flags if f.flag_type == flag_type])
            
            # Network breakdown
            network_breakdown = {}
            for network_name in ["stellar", "hedera"]:
                network_breakdown[network_name] = len([f for f in flags if f.network == network_name])
            
            # Country breakdown (top 10)
            country_counts = {}
            for flag in flags:
                if flag.country_code:
                    country_counts[flag.country_code] = country_counts.get(flag.country_code, 0) + 1
            
            top_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Average risk score
            risk_scores = [float(f.risk_score) for f in flags if f.risk_score is not None]
            avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0
            
            return {
                "success": True,
                "summary": {
                    "total_flags": total_flags,
                    "active_flags": active_flags,
                    "resolved_flags": resolved_flags,
                    "closed_flags": closed_flags,
                    "avg_risk_score": round(avg_risk_score, 2)
                },
                "severity_breakdown": severity_breakdown,
                "type_breakdown": type_breakdown,
                "network_breakdown": network_breakdown,
                "top_countries": [{"country": country, "count": count} for country, count in top_countries],
                "period": {
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get flag analytics: {str(e)}"
            }
    
    async def _get_flag_history(self, flag_id: str) -> List[Dict[str, Any]]:
        """Get audit trail/history for a flag"""
        # For MVP, return mock history
        # In production, this would query an audit log table
        return [
            {
                "action": "created",
                "timestamp": datetime.now().isoformat(),
                "user": "system",
                "details": "Flag created automatically"
            }
        ]
    
    async def _get_entity_info(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        """Get information about the flagged entity"""
        # For MVP, return basic entity info
        # In production, this would query the appropriate entity table
        return {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "entity_name": f"{entity_type}_{entity_id}",
            "last_activity": datetime.now().isoformat()
        }
    
    async def get_compliance_reports(self, **kwargs) -> List[Dict[str, Any]]:
        """Get compliance reports"""
        # Placeholder implementation
        return []
