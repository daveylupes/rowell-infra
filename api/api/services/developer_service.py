"""
Developer service for handling developer operations
"""

import secrets
import hashlib
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from api.models.developer import Developer, Project, APIKey, DeveloperSession
from api.schemas.developer import (
    DeveloperRegistrationRequest, 
    ProjectCreateRequest, 
    APIKeyCreateRequest
)
import structlog
from datetime import datetime, timedelta
import uuid

logger = structlog.get_logger()


class DeveloperService:
    """Service for managing developers, projects, and API keys"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register_developer(self, request: DeveloperRegistrationRequest) -> Dict[str, Any]:
        """Register a new developer"""
        try:
            logger.info("Registering new developer", email=request.email)
            
            # Check if developer already exists
            result = await self.db.execute(
                select(Developer).where(Developer.email == request.email)
            )
            existing_developer = result.scalar_one_or_none()
            
            if existing_developer:
                raise ValueError("Developer with this email already exists")
            
            # Create new developer
            developer = Developer(
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
                company=request.company,
                role=request.role,
                country_code=request.country_code,
                phone=request.phone,
                is_active=True,
                is_verified=False
            )
            
            self.db.add(developer)
            await self.db.commit()
            await self.db.refresh(developer)
            
            logger.info("Developer registered successfully", developer_id=str(developer.id))
            
            return {
                "id": str(developer.id),
                "email": developer.email,
                "first_name": developer.first_name,
                "last_name": developer.last_name,
                "company": developer.company,
                "role": developer.role,
                "country_code": developer.country_code,
                "phone": developer.phone,
                "is_active": developer.is_active,
                "is_verified": developer.is_verified,
                "created_at": developer.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to register developer", error=str(e))
            await self.db.rollback()
            raise
    
    async def get_developer(self, developer_id: str) -> Optional[Dict[str, Any]]:
        """Get developer by ID"""
        try:
            result = await self.db.execute(
                select(Developer).where(Developer.id == developer_id)
            )
            developer = result.scalar_one_or_none()
            
            if not developer:
                return None
            
            return {
                "id": str(developer.id),
                "email": developer.email,
                "first_name": developer.first_name,
                "last_name": developer.last_name,
                "company": developer.company,
                "role": developer.role,
                "country_code": developer.country_code,
                "phone": developer.phone,
                "is_active": developer.is_active,
                "is_verified": developer.is_verified,
                "email_verified_at": developer.email_verified_at.isoformat() if developer.email_verified_at else None,
                "created_at": developer.created_at.isoformat(),
                "updated_at": developer.updated_at.isoformat() if developer.updated_at else None,
                "last_login": developer.last_login.isoformat() if developer.last_login else None
            }
            
        except Exception as e:
            logger.error("Failed to get developer", developer_id=developer_id, error=str(e))
            raise

    async def get_developer_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get developer by email address"""
        try:
            result = await self.db.execute(
                select(Developer).where(Developer.email == email)
            )
            developer = result.scalar_one_or_none()
            
            if not developer:
                return None
            
            return {
                "id": str(developer.id),
                "email": developer.email,
                "first_name": developer.first_name,
                "last_name": developer.last_name,
                "company": developer.company,
                "role": developer.role,
                "country_code": developer.country_code,
                "phone": developer.phone,
                "is_active": developer.is_active,
                "is_verified": developer.is_verified,
                "email_verified_at": developer.email_verified_at.isoformat() if developer.email_verified_at else None,
                "created_at": developer.created_at.isoformat(),
                "updated_at": developer.updated_at.isoformat() if developer.updated_at else None,
                "last_login": developer.last_login.isoformat() if developer.last_login else None
            }
            
        except Exception as e:
            logger.error("Failed to get developer by email", email=email, error=str(e))
            raise
    
    async def create_project(self, developer_id: str, request: ProjectCreateRequest) -> Dict[str, Any]:
        """Create a new project for a developer"""
        try:
            logger.info("Creating new project", developer_id=developer_id, name=request.name)
            
            # Verify developer exists
            result = await self.db.execute(
                select(Developer).where(Developer.id == developer_id)
            )
            developer = result.scalar_one_or_none()
            
            if not developer:
                raise ValueError("Developer not found")
            
            # Create new project
            project = Project(
                developer_id=developer_id,
                name=request.name,
                description=request.description,
                primary_network=request.primary_network,
                environment=request.environment,
                webhook_url=request.webhook_url,
                is_active=True,
                is_public=False
            )
            
            self.db.add(project)
            await self.db.commit()
            await self.db.refresh(project)
            
            logger.info("Project created successfully", project_id=str(project.id))
            
            return {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "primary_network": project.primary_network,
                "environment": project.environment,
                "webhook_url": project.webhook_url,
                "is_active": project.is_active,
                "is_public": project.is_public,
                "created_at": project.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to create project", error=str(e))
            await self.db.rollback()
            raise
    
    async def generate_api_key(self, developer_id: str, project_id: str, request: APIKeyCreateRequest) -> Dict[str, Any]:
        """Generate a new API key for a project"""
        try:
            logger.info("Generating API key", developer_id=developer_id, project_id=project_id)
            
            # Verify project belongs to developer
            result = await self.db.execute(
                select(Project).where(
                    and_(
                        Project.id == project_id,
                        Project.developer_id == developer_id
                    )
                )
            )
            project = result.scalar_one_or_none()
            
            if not project:
                raise ValueError("Project not found or access denied")
            
            # Generate API key
            api_key = f"ri_{secrets.token_urlsafe(32)}"
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            key_prefix = api_key[:8]
            
            # Create API key record
            api_key_record = APIKey(
                developer_id=developer_id,
                project_id=project_id,
                key_name=request.key_name,
                key_hash=key_hash,
                key_prefix=key_prefix,
                permissions=request.permissions,
                rate_limit=request.rate_limit,
                is_active=True,
                expires_at=request.expires_at
            )
            
            self.db.add(api_key_record)
            await self.db.commit()
            await self.db.refresh(api_key_record)
            
            logger.info("API key generated successfully", api_key_id=str(api_key_record.id))
            
            return {
                "id": str(api_key_record.id),
                "key_name": api_key_record.key_name,
                "api_key": api_key,  # Only returned once
                "key_prefix": api_key_record.key_prefix,
                "permissions": api_key_record.permissions,
                "rate_limit": api_key_record.rate_limit,
                "is_active": api_key_record.is_active,
                "created_at": api_key_record.created_at.isoformat(),
                "expires_at": api_key_record.expires_at.isoformat() if api_key_record.expires_at else None
            }
            
        except Exception as e:
            logger.error("Failed to generate API key", error=str(e))
            await self.db.rollback()
            raise
    
    async def get_developer_projects(self, developer_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a developer"""
        try:
            result = await self.db.execute(
                select(Project).where(Project.developer_id == developer_id)
            )
            projects = result.scalars().all()
            
            return [
                {
                    "id": str(project.id),
                    "name": project.name,
                    "description": project.description,
                    "primary_network": project.primary_network,
                    "environment": project.environment,
                    "webhook_url": project.webhook_url,
                    "is_active": project.is_active,
                    "is_public": project.is_public,
                    "created_at": project.created_at.isoformat(),
                    "updated_at": project.updated_at.isoformat() if project.updated_at else None
                }
                for project in projects
            ]
            
        except Exception as e:
            logger.error("Failed to get developer projects", error=str(e))
            raise
    
    async def get_project_api_keys(self, developer_id: str, project_id: str) -> List[Dict[str, Any]]:
        """Get all API keys for a project"""
        try:
            # Verify project belongs to developer
            result = await self.db.execute(
                select(Project).where(
                    and_(
                        Project.id == project_id,
                        Project.developer_id == developer_id
                    )
                )
            )
            project = result.scalar_one_or_none()
            
            if not project:
                raise ValueError("Project not found or access denied")
            
            result = await self.db.execute(
                select(APIKey).where(APIKey.project_id == project_id)
            )
            api_keys = result.scalars().all()
            
            return [
                {
                    "id": str(api_key.id),
                    "key_name": api_key.key_name,
                    "key_prefix": api_key.key_prefix,
                    "permissions": api_key.permissions,
                    "rate_limit": api_key.rate_limit,
                    "is_active": api_key.is_active,
                    "last_used": api_key.last_used.isoformat() if api_key.last_used else None,
                    "usage_count": api_key.usage_count,
                    "created_at": api_key.created_at.isoformat(),
                    "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None
                }
                for api_key in api_keys
            ]
            
        except Exception as e:
            logger.error("Failed to get project API keys", error=str(e))
            raise
    
    async def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key and return associated project info"""
        try:
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            result = await self.db.execute(
                select(APIKey)
                .options(selectinload(APIKey.project), selectinload(APIKey.developer))
                .where(
                    and_(
                        APIKey.key_hash == key_hash,
                        APIKey.is_active == True
                    )
                )
            )
            api_key_record = result.scalar_one_or_none()
            
            if not api_key_record:
                return None
            
            # Check if key is expired
            if api_key_record.expires_at and api_key_record.expires_at < datetime.utcnow():
                return None
            
            # Update usage stats
            api_key_record.usage_count += 1
            api_key_record.last_used = datetime.utcnow()
            await self.db.commit()
            
            return {
                "developer_id": str(api_key_record.developer_id),
                "project_id": str(api_key_record.project_id),
                "permissions": api_key_record.permissions,
                "rate_limit": api_key_record.rate_limit,
                "project_name": api_key_record.project.name,
                "developer_name": f"{api_key_record.developer.first_name} {api_key_record.developer.last_name}"
            }
            
        except Exception as e:
            logger.error("Failed to validate API key", error=str(e))
            raise
    
    async def get_developer_dashboard(self, developer_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a developer"""
        try:
            # Get developer info
            developer = await self.get_developer(developer_id)
            if not developer:
                raise ValueError("Developer not found")
            
            # Get projects
            projects = await self.get_developer_projects(developer_id)
            
            # Get all API keys for all projects
            all_api_keys = []
            for project in projects:
                project_api_keys = await self.get_project_api_keys(developer_id, project["id"])
                all_api_keys.extend(project_api_keys)
            
            # Calculate stats
            stats = {
                "total_projects": len(projects),
                "total_api_keys": len(all_api_keys),
                "active_api_keys": len([key for key in all_api_keys if key["is_active"]]),
                "total_usage": sum(key["usage_count"] for key in all_api_keys)
            }
            
            return {
                "developer": developer,
                "projects": projects,
                "api_keys": all_api_keys,
                "stats": stats
            }
            
        except Exception as e:
            logger.error("Failed to get developer dashboard", error=str(e))
            raise
