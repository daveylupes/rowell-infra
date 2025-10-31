"""
Tests for authentication system
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from api.main import app
from api.core.database import get_db
from api.models.user import User, Role, Permission
from api.services.user_service import UserService
from api.schemas.user import UserCreate
import asyncio

client = TestClient(app)


@pytest.fixture
async def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
        "company": "Test Company",
        "country_code": "US"
    }


@pytest.fixture
async def test_db_session():
    """Get test database session"""
    # This would need to be properly configured with test database
    # For now, this is a placeholder
    pass


class TestUserRegistration:
    """Test user registration functionality"""
    
    @pytest.mark.asyncio
    async def test_user_registration_success(self, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["first_name"] == test_user_data["first_name"]
        assert data["last_name"] == test_user_data["last_name"]
        assert "id" in data
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "password_hash" not in data  # Password should not be returned
    
    def test_user_registration_duplicate_email(self, test_user_data):
        """Test registration with duplicate email"""
        # First registration
        response1 = client.post("/api/v1/auth/register", json=test_user_data)
        assert response1.status_code == 201
        
        # Second registration with same email
        response2 = client.post("/api/v1/auth/register", json=test_user_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]
    
    def test_user_registration_invalid_password(self, test_user_data):
        """Test registration with invalid password"""
        invalid_data = test_user_data.copy()
        invalid_data["password"] = "weak"  # Too weak
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_user_registration_invalid_email(self, test_user_data):
        """Test registration with invalid email"""
        invalid_data = test_user_data.copy()
        invalid_data["email"] = "invalid-email"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login functionality"""
    
    def test_user_login_success(self, test_user_data):
        """Test successful user login"""
        # First register a user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 201
        
        # Then login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 900  # 15 minutes
    
    def test_user_login_invalid_credentials(self, test_user_data):
        """Test login with invalid credentials"""
        # First register a user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 201
        
        # Then try to login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_user_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]


class TestTokenRefresh:
    """Test token refresh functionality"""
    
    def test_token_refresh_success(self, test_user_data):
        """Test successful token refresh"""
        # Register and login
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 201
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        assert login_response.status_code == 200
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_token_refresh_invalid_token(self):
        """Test token refresh with invalid token"""
        response = client.post("/api/v1/auth/refresh", json={
            "refresh_token": "invalid_token"
        })
        
        assert response.status_code == 401
        assert "Invalid or expired refresh token" in response.json()["detail"]


class TestUserProfile:
    """Test user profile functionality"""
    
    def test_get_current_user(self, test_user_data):
        """Test getting current user information"""
        # Register and login
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 201
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        assert login_response.status_code == 200
        
        access_token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["first_name"] == test_user_data["first_name"]
        assert data["last_name"] == test_user_data["last_name"]
    
    def test_get_current_user_unauthorized(self):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401


class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_request_password_reset(self, test_user_data):
        """Test requesting password reset"""
        # Register a user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 201
        
        # Request password reset
        response = client.post("/api/v1/auth/request-password-reset", json={
            "email": test_user_data["email"]
        })
        
        assert response.status_code == 200
        assert "password reset link has been sent" in response.json()["message"]
    
    def test_request_password_reset_nonexistent_email(self):
        """Test requesting password reset for nonexistent email"""
        response = client.post("/api/v1/auth/request-password-reset", json={
            "email": "nonexistent@example.com"
        })
        
        # Should still return success to prevent email enumeration
        assert response.status_code == 200
        assert "password reset link has been sent" in response.json()["message"]


class TestUserService:
    """Test UserService functionality"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_db_session):
        """Test creating a user through UserService"""
        user_service = UserService(test_db_session)
        user_data = UserCreate(
            email="service@example.com",
            password="TestPassword123!",
            first_name="Service",
            last_name="Test",
            company="Test Company"
        )
        
        user = await user_service.create_user(user_data)
        assert user.email == user_data.email
        assert user.first_name == user_data.first_name
        assert user.last_name == user_data.last_name
        assert user.is_active is True
        assert user.is_verified is False
    
    @pytest.mark.asyncio
    async def test_authenticate_user(self, test_db_session):
        """Test user authentication through UserService"""
        user_service = UserService(test_db_session)
        
        # Create user
        user_data = UserCreate(
            email="auth@example.com",
            password="TestPassword123!",
            first_name="Auth",
            last_name="Test"
        )
        user = await user_service.create_user(user_data)
        
        # Test authentication
        authenticated_user = await user_service.authenticate_user(
            user_data.email, 
            user_data.password
        )
        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        
        # Test wrong password
        wrong_auth = await user_service.authenticate_user(
            user_data.email, 
            "wrongpassword"
        )
        assert wrong_auth is None
