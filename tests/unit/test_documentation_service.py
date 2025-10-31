"""
Unit tests for API Documentation functionality
"""

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.main import create_application
from api.docs import CodeExamples, ErrorCodes, AuthenticationGuide, RateLimitingGuide


class TestCodeExamples:
    """Test cases for CodeExamples class"""
    
    def test_get_javascript_examples(self):
        """Test getting JavaScript code examples"""
        examples = CodeExamples.get_javascript_examples()
        
        assert isinstance(examples, dict)
        assert "account_creation" in examples
        assert "transfer_creation" in examples
        assert "account_listing" in examples
        
        # Check account creation example
        account_example = examples["account_creation"]
        assert "title" in account_example
        assert "description" in account_example
        assert "code" in account_example
        assert "Create Account (JavaScript)" in account_example["title"]
        assert "fetch" in account_example["code"]
        assert "axios" in account_example["code"]
    
    def test_get_python_examples(self):
        """Test getting Python code examples"""
        examples = CodeExamples.get_python_examples()
        
        assert isinstance(examples, dict)
        assert "account_creation" in examples
        assert "transfer_creation" in examples
        assert "kyc_verification" in examples
        
        # Check transfer creation example
        transfer_example = examples["transfer_creation"]
        assert "title" in transfer_example
        assert "description" in transfer_example
        assert "code" in transfer_example
        assert "Create Transfer (Python)" in transfer_example["title"]
        assert "requests.post" in transfer_example["code"]
    
    def test_get_curl_examples(self):
        """Test getting cURL code examples"""
        examples = CodeExamples.get_curl_examples()
        
        assert isinstance(examples, dict)
        assert "account_creation" in examples
        assert "transfer_creation" in examples
        assert "account_listing" in examples
        
        # Check account listing example
        listing_example = examples["account_listing"]
        assert "title" in listing_example
        assert "description" in listing_example
        assert "code" in listing_example
        assert "curl -X GET" in listing_example["code"]
    
    def test_get_all_examples(self):
        """Test getting all code examples"""
        all_examples = CodeExamples.get_all_examples()
        
        assert isinstance(all_examples, dict)
        assert "javascript" in all_examples
        assert "python" in all_examples
        assert "curl" in all_examples
        
        # Verify structure
        for language, examples in all_examples.items():
            assert isinstance(examples, dict)
            assert len(examples) > 0


class TestErrorCodes:
    """Test cases for ErrorCodes class"""
    
    def test_get_error_codes(self):
        """Test getting all error codes"""
        error_codes = ErrorCodes.get_error_codes()
        
        assert isinstance(error_codes, dict)
        assert len(error_codes) > 0
        
        # Check a specific error code
        auth_required = error_codes["AUTH_REQUIRED"]
        assert auth_required["http_status"] == 401
        assert "Authentication Required" in auth_required["title"]
        assert "solution" in auth_required
        assert "example" in auth_required
    
    def test_get_error_by_code(self):
        """Test getting specific error by code"""
        error_info = ErrorCodes.get_error_by_code("AUTH_REQUIRED")
        
        assert error_info["http_status"] == 401
        assert "Authentication Required" in error_info["title"]
        assert "solution" in error_info
        
        # Test unknown error code
        unknown_error = ErrorCodes.get_error_by_code("UNKNOWN_ERROR")
        assert unknown_error["http_status"] == 500
        assert "Unknown Error" in unknown_error["title"]
    
    def test_get_errors_by_status_code(self):
        """Test getting errors by HTTP status code"""
        errors_401 = ErrorCodes.get_errors_by_status_code(401)
        
        assert isinstance(errors_401, list)
        assert len(errors_401) > 0
        
        for error in errors_401:
            assert "code" in error
            assert error["http_status"] == 401
        
        errors_404 = ErrorCodes.get_errors_by_status_code(404)
        assert isinstance(errors_404, list)
    
    def test_get_troubleshooting_guide(self):
        """Test getting troubleshooting guide"""
        guide = ErrorCodes.get_troubleshooting_guide()
        
        assert isinstance(guide, dict)
        assert "common_issues" in guide
        assert "best_practices" in guide
        assert "debugging_tips" in guide
        
        # Check common issues structure
        common_issues = guide["common_issues"]
        assert isinstance(common_issues, list)
        assert len(common_issues) > 0
        
        for issue in common_issues:
            assert "issue" in issue
            assert "causes" in issue
            assert "solutions" in issue


class TestAuthenticationGuide:
    """Test cases for AuthenticationGuide class"""
    
    def test_get_authentication_overview(self):
        """Test getting authentication overview"""
        overview = AuthenticationGuide.get_authentication_overview()
        
        assert isinstance(overview, dict)
        assert "overview" in overview
        assert "requirements" in overview
        assert "supported_environments" in overview
        
        # Check overview structure
        overview_info = overview["overview"]
        assert "title" in overview_info
        assert "API Authentication" in overview_info["title"]
        assert "authentication_method" in overview_info
    
    def test_get_api_key_guide(self):
        """Test getting API key guide"""
        guide = AuthenticationGuide.get_api_key_guide()
        
        assert isinstance(guide, dict)
        assert "getting_api_key" in guide
        assert "api_key_format" in guide
        assert "permissions" in guide
        
        # Check getting API key steps
        getting_key = guide["getting_api_key"]
        assert "title" in getting_key
        assert "steps" in getting_key
        assert isinstance(getting_key["steps"], list)
        assert len(getting_key["steps"]) > 0
    
    def test_get_authentication_examples(self):
        """Test getting authentication examples"""
        examples = AuthenticationGuide.get_authentication_examples()
        
        assert isinstance(examples, dict)
        assert "curl" in examples
        assert "javascript" in examples
        assert "python" in examples
        
        # Check JavaScript examples
        js_examples = examples["javascript"]
        assert "title" in js_examples
        assert "fetch_api" in js_examples
        assert "axios" in js_examples
    
    def test_get_security_best_practices(self):
        """Test getting security best practices"""
        practices = AuthenticationGuide.get_security_best_practices()
        
        assert isinstance(practices, dict)
        assert "api_key_security" in practices
        assert "secure_storage" in practices
        assert "common_mistakes" in practices
        assert "troubleshooting" in practices
        
        # Check security practices
        security_list = practices["api_key_security"]
        assert isinstance(security_list, list)
        assert len(security_list) > 0
    
    def test_get_authentication_flow(self):
        """Test getting authentication flow"""
        flow = AuthenticationGuide.get_authentication_flow()
        
        assert isinstance(flow, dict)
        assert "flow_diagram" in flow
        assert "flow_steps" in flow
        assert "error_handling" in flow
        
        # Check flow steps
        steps = flow["flow_steps"]
        assert isinstance(steps, list)
        assert len(steps) > 0
        
        for step in steps:
            assert "step" in step
            assert "title" in step
            assert "description" in step


class TestRateLimitingGuide:
    """Test cases for RateLimitingGuide class"""
    
    def test_get_rate_limiting_overview(self):
        """Test getting rate limiting overview"""
        overview = RateLimitingGuide.get_rate_limiting_overview()
        
        assert isinstance(overview, dict)
        assert "overview" in overview
        assert "rate_limit_types" in overview
        assert "identification" in overview
        
        # Check overview structure
        overview_info = overview["overview"]
        assert "title" in overview_info
        assert "Rate Limiting" in overview_info["title"]
    
    def test_get_rate_limits_by_plan(self):
        """Test getting rate limits by plan"""
        plans = RateLimitingGuide.get_rate_limits_by_plan()
        
        assert isinstance(plans, dict)
        assert "free_tier" in plans
        assert "pro_tier" in plans
        assert "enterprise_tier" in plans
        
        # Check free tier limits
        free_tier = plans["free_tier"]
        assert "limits" in free_tier
        assert free_tier["limits"]["requests_per_minute"] == 100
    
    def test_get_rate_limit_headers(self):
        """Test getting rate limit headers"""
        headers = RateLimitingGuide.get_rate_limit_headers()
        
        assert isinstance(headers, dict)
        assert "headers" in headers
        assert "example_response" in headers
        assert "rate_limit_exceeded_response" in headers
        
        # Check header definitions
        header_defs = headers["headers"]
        assert "X-RateLimit-Limit" in header_defs
        assert "X-RateLimit-Remaining" in header_defs
        assert "Retry-After" in header_defs
    
    def test_get_best_practices(self):
        """Test getting best practices"""
        practices = RateLimitingGuide.get_best_practices()
        
        assert isinstance(practices, dict)
        assert "monitoring" in practices
        assert "optimization" in practices
        assert "error_handling" in practices
        assert "code_examples" in practices
        
        # Check monitoring practices
        monitoring = practices["monitoring"]
        assert isinstance(monitoring, list)
        assert len(monitoring) > 0
    
    def test_get_implementation_examples(self):
        """Test getting implementation examples"""
        examples = RateLimitingGuide.get_implementation_examples()
        
        assert isinstance(examples, dict)
        assert "exponential_backoff" in examples
        assert "request_batching" in examples
        
        # Check exponential backoff example
        backoff = examples["exponential_backoff"]
        assert "javascript" in backoff
        assert "python" in backoff
    
    def test_get_monitoring_recommendations(self):
        """Test getting monitoring recommendations"""
        monitoring = RateLimitingGuide.get_monitoring_recommendations()
        
        assert isinstance(monitoring, dict)
        assert "metrics_to_track" in monitoring
        assert "alert_thresholds" in monitoring
        assert "monitoring_tools" in monitoring
        assert "dashboard_example" in monitoring


class TestDocumentationEndpoints:
    """Test cases for documentation API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_application()
        return TestClient(app)
    
    def test_get_code_examples_endpoint(self, client):
        """Test code examples endpoint"""
        response = client.get("/api/v1/docs/examples")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "examples" in data
        assert "supported_languages" in data
        assert "available_endpoints" in data
    
    def test_get_code_examples_with_language_filter(self, client):
        """Test code examples endpoint with language filter"""
        response = client.get("/api/v1/docs/examples?language=javascript")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "javascript" in data["examples"]
        assert "python" not in data["examples"]
    
    def test_get_code_examples_invalid_language(self, client):
        """Test code examples endpoint with invalid language"""
        response = client.get("/api/v1/docs/examples?language=invalid")
        
        assert response.status_code == 400
        data = response.json()
        
        assert "Unsupported language" in data["detail"]
    
    def test_get_error_codes_endpoint(self, client):
        """Test error codes endpoint"""
        response = client.get("/api/v1/docs/error-codes")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "error_codes" in data
        assert "troubleshooting_guide" in data
        assert "total_errors" in data
    
    def test_get_error_codes_by_status(self, client):
        """Test error codes endpoint with status filter"""
        response = client.get("/api/v1/docs/error-codes?status_code=401")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "status_code" in data
        assert data["status_code"] == 401
        assert "errors" in data
    
    def test_get_error_codes_by_code(self, client):
        """Test error codes endpoint with specific error code"""
        response = client.get("/api/v1/docs/error-codes?error_code=AUTH_REQUIRED")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["error_code"] == "AUTH_REQUIRED"
        assert "information" in data
    
    def test_get_authentication_guide_endpoint(self, client):
        """Test authentication guide endpoint"""
        response = client.get("/api/v1/docs/authentication")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "overview" in data
        assert "api_key_guide" in data
        assert "examples" in data
        assert "best_practices" in data
        assert "authentication_flow" in data
    
    def test_get_rate_limiting_guide_endpoint(self, client):
        """Test rate limiting guide endpoint"""
        response = client.get("/api/v1/docs/rate-limiting")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "overview" in data
        assert "plans" in data
        assert "headers" in data
        assert "best_practices" in data
        assert "implementation_examples" in data
        assert "monitoring" in data
    
    def test_get_interactive_documentation_endpoint(self, client):
        """Test interactive documentation endpoint"""
        response = client.get("/api/v1/docs/interactive")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "interactive_docs" in data
        assert "quick_start" in data
    
    def test_get_api_status_endpoint(self, client):
        """Test API status endpoint"""
        response = client.get("/api/v1/docs/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "status" in data
        assert "version" in data
        assert "services" in data
        assert "uptime" in data
        assert "rate_limits" in data
    
    def test_get_api_changelog_endpoint(self, client):
        """Test API changelog endpoint"""
        response = client.get("/api/v1/docs/changelog")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "changelog" in data
        assert "upcoming_features" in data
        assert "deprecation_notices" in data
    
    def test_get_sdk_information_endpoint(self, client):
        """Test SDK information endpoint"""
        response = client.get("/api/v1/docs/sdk")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "official_sdks" in data
        assert "community_sdks" in data
        assert "installation_examples" in data
