"""
Developer management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import structlog

from api.core.database import get_db
from api.services.developer_service import DeveloperService
from api.schemas.developer import (
    DeveloperRegistrationRequest,
    DeveloperResponse,
    ProjectCreateRequest,
    ProjectResponse,
    APIKeyCreateRequest,
    APIKeyWithSecretResponse,
    DeveloperDashboardResponse,
    QuickStartResponse
)

logger = structlog.get_logger()
router = APIRouter()


@router.post("/register", response_model=DeveloperResponse)
async def register_developer(
    request: DeveloperRegistrationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Register a new developer"""
    try:
        developer_service = DeveloperService(db)
        developer_data = await developer_service.register_developer(request)
        
        # TODO: Send verification email in background
        # background_tasks.add_task(send_verification_email, developer_data["email"])
        
        return DeveloperResponse(**developer_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to register developer", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register developer"
        )


@router.get("/{developer_id}", response_model=DeveloperResponse)
async def get_developer(
    developer_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get developer information"""
    try:
        developer_service = DeveloperService(db)
        developer_data = await developer_service.get_developer(developer_id)
        
        if not developer_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Developer not found"
            )
        
        return DeveloperResponse(**developer_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get developer", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get developer"
        )


@router.get("/by-email/{email}", response_model=DeveloperResponse)
async def get_developer_by_email(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Get developer by email address"""
    try:
        developer_service = DeveloperService(db)
        developer_data = await developer_service.get_developer_by_email(email)
        
        if not developer_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Developer not found"
            )
        
        return DeveloperResponse(**developer_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get developer by email", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get developer"
        )


@router.post("/{developer_id}/projects", response_model=ProjectResponse)
async def create_project(
    developer_id: str,
    request: ProjectCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project for a developer"""
    try:
        developer_service = DeveloperService(db)
        project_data = await developer_service.create_project(developer_id, request)
        
        return ProjectResponse(**project_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to create project", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


@router.get("/{developer_id}/projects", response_model=List[ProjectResponse])
async def get_developer_projects(
    developer_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all projects for a developer"""
    try:
        developer_service = DeveloperService(db)
        projects_data = await developer_service.get_developer_projects(developer_id)
        
        return [ProjectResponse(**project) for project in projects_data]
        
    except Exception as e:
        logger.error("Failed to get developer projects", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get developer projects"
        )


@router.post("/{developer_id}/projects/{project_id}/api-keys", response_model=APIKeyWithSecretResponse)
async def generate_api_key(
    developer_id: str,
    project_id: str,
    request: APIKeyCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a new API key for a project"""
    try:
        developer_service = DeveloperService(db)
        api_key_data = await developer_service.generate_api_key(developer_id, project_id, request)
        
        return APIKeyWithSecretResponse(**api_key_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to generate API key", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate API key"
        )


@router.get("/{developer_id}/dashboard", response_model=DeveloperDashboardResponse)
async def get_developer_dashboard(
    developer_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive dashboard data for a developer"""
    try:
        developer_service = DeveloperService(db)
        dashboard_data = await developer_service.get_developer_dashboard(developer_id)
        
        return DeveloperDashboardResponse(**dashboard_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to get developer dashboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get developer dashboard"
        )


@router.post("/quickstart", response_model=QuickStartResponse)
async def quickstart_developer(
    request: DeveloperRegistrationRequest,
    project_name: str = "My First Project",
    db: AsyncSession = Depends(get_db)
):
    """Quick start flow: register developer, create project, and generate API key"""
    try:
        developer_service = DeveloperService(db)
        
        # Register developer
        developer_data = await developer_service.register_developer(request)
        developer_id = developer_data["id"]
        
        # Create default project
        project_request = ProjectCreateRequest(
            name=project_name,
            description="My first Rowell Infra project",
            primary_network="stellar",
            environment="testnet"
        )
        project_data = await developer_service.create_project(developer_id, project_request)
        project_id = project_data["id"]
        
        # Generate API key with default permissions
        api_key_request = APIKeyCreateRequest(
            key_name="Default API Key",
            permissions=["accounts:read", "accounts:write", "transfers:read", "transfers:write"],
            rate_limit=1000
        )
        api_key_data = await developer_service.generate_api_key(developer_id, project_id, api_key_request)
        
        # Generate example code
        example_code = {
            "javascript": f"""
// Install: npm install @rowell-infra/sdk
import {{ RowellInfra }} from '@rowell-infra/sdk';

const client = new RowellInfra({{
  apiKey: '{api_key_data["api_key"]}',
  environment: 'testnet'
}});

// Create your first account
const account = await client.accounts.create({{
  network: 'stellar',
  environment: 'testnet',
  accountType: 'user',
  countryCode: 'NG'
}});

console.log('Account created:', account);
""",
            "python": f"""
# Install: pip install rowell-infra
from rowell_infra import RowellInfra

client = RowellInfra(
    api_key='{api_key_data["api_key"]}',
    environment='testnet'
)

# Create your first account
account = client.accounts.create(
    network='stellar',
    environment='testnet',
    account_type='user',
    country_code='NG'
)

print('Account created:', account)
""",
            "curl": f"""
# Create your first account
curl -X POST "https://api.rowell-infra.com/v1/accounts/create" \\
  -H "Authorization: Bearer {api_key_data["api_key"]}" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG"
  }}'
"""
        }
        
        return QuickStartResponse(
            developer=DeveloperResponse(**developer_data),
            project=ProjectResponse(**project_data),
            api_key=APIKeyWithSecretResponse(**api_key_data),
            example_code=example_code
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to complete quickstart", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete quickstart"
        )
