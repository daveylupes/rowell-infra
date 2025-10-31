"""
Rate limiting guide for Rowell Infra API
"""

from typing import Dict, List, Any


class RateLimitingGuide:
    """Comprehensive rate limiting documentation and best practices"""
    
    @staticmethod
    def get_rate_limiting_overview() -> Dict[str, Any]:
        """Get rate limiting overview and policies"""
        return {
            "overview": {
                "title": "Rate Limiting",
                "description": "The Rowell Infra API implements rate limiting to ensure fair usage and maintain service quality for all users.",
                "purpose": [
                    "Prevent API abuse and ensure fair usage",
                    "Maintain service stability and performance",
                    "Protect against DDoS attacks",
                    "Ensure consistent response times"
                ]
            },
            "rate_limit_types": {
                "per_minute": "Requests per minute (RPM)",
                "per_hour": "Requests per hour (RPH)",
                "per_day": "Requests per day (RPD)",
                "burst": "Short-term burst allowance"
            },
            "identification": {
                "method": "Rate limits are applied per API key",
                "tracking": "Requests are tracked using the X-API-Key header",
                "isolation": "Each API key has independent rate limits"
            }
        }
    
    @staticmethod
    def get_rate_limits_by_plan() -> Dict[str, Any]:
        """Get rate limits for different subscription plans"""
        return {
            "free_tier": {
                "name": "Free Tier",
                "description": "Basic access for development and testing",
                "limits": {
                    "requests_per_minute": 100,
                    "requests_per_hour": 6000,
                    "requests_per_day": 100000,
                    "burst_limit": 150
                },
                "features": [
                    "Testnet access only",
                    "Basic analytics",
                    "Standard support"
                ]
            },
            "pro_tier": {
                "name": "Pro Tier",
                "description": "Enhanced limits for production applications",
                "limits": {
                    "requests_per_minute": 1000,
                    "requests_per_hour": 60000,
                    "requests_per_day": 1000000,
                    "burst_limit": 1500
                },
                "features": [
                    "Mainnet and testnet access",
                    "Advanced analytics",
                    "Priority support",
                    "Custom webhooks"
                ]
            },
            "enterprise_tier": {
                "name": "Enterprise Tier",
                "description": "Custom limits for high-volume applications",
                "limits": {
                    "requests_per_minute": "Custom",
                    "requests_per_hour": "Custom",
                    "requests_per_day": "Custom",
                    "burst_limit": "Custom"
                },
                "features": [
                    "Custom rate limits",
                    "Dedicated support",
                    "SLA guarantees",
                    "Custom integrations",
                    "On-premise deployment options"
                ]
            }
        }
    
    @staticmethod
    def get_rate_limit_headers() -> Dict[str, Any]:
        """Get rate limit response headers documentation"""
        return {
            "headers": {
                "X-RateLimit-Limit": {
                    "description": "The rate limit ceiling for the given request",
                    "example": "X-RateLimit-Limit: 1000",
                    "type": "integer"
                },
                "X-RateLimit-Remaining": {
                    "description": "The number of requests left in the current rate limit window",
                    "example": "X-RateLimit-Remaining: 999",
                    "type": "integer"
                },
                "X-RateLimit-Reset": {
                    "description": "The time at which the current rate limit window resets (Unix timestamp)",
                    "example": "X-RateLimit-Reset: 1640995200",
                    "type": "integer"
                },
                "X-RateLimit-Window": {
                    "description": "The time window for the rate limit in seconds",
                    "example": "X-RateLimit-Window: 60",
                    "type": "integer"
                },
                "Retry-After": {
                    "description": "Number of seconds to wait before retrying (only present on 429 responses)",
                    "example": "Retry-After: 30",
                    "type": "integer"
                }
            },
            "example_response": """
HTTP/1.1 200 OK
Content-Type: application/json
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Window: 60

{
  "accounts": [...],
  "pagination": {...}
}
""",
            "rate_limit_exceeded_response": """
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995260
X-RateLimit-Window: 60
Retry-After: 30

{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "details": {
    "limit": 1000,
    "window": 60,
    "reset_time": "2024-01-01T01:01:00Z"
  }
}
"""
        }
    
    @staticmethod
    def get_best_practices() -> Dict[str, Any]:
        """Get rate limiting best practices and strategies"""
        return {
            "monitoring": [
                "Always check rate limit headers in responses",
                "Monitor your API usage patterns",
                "Set up alerts for approaching limits",
                "Track usage trends over time"
            ],
            "optimization": [
                "Use pagination to reduce request frequency",
                "Implement efficient caching strategies",
                "Batch multiple operations when possible",
                "Use webhooks instead of polling where applicable"
            ],
            "error_handling": [
                "Implement exponential backoff for retries",
                "Respect the Retry-After header",
                "Log rate limit errors for analysis",
                "Have fallback strategies for rate limit scenarios"
            ],
            "code_examples": {
                "javascript": """
// Check rate limit headers
const response = await fetch('/api/v1/accounts', {
  headers: { 'X-API-Key': apiKey }
});

const rateLimitRemaining = response.headers.get('X-RateLimit-Remaining');
const rateLimitReset = response.headers.get('X-RateLimit-Reset');

if (parseInt(rateLimitRemaining) < 10) {
  console.warn('Rate limit approaching');
}

// Handle rate limit exceeded
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
  // Retry the request
}
""",
                "python": """
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class RateLimitedClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def make_request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-API-Key'] = self.api_key
        kwargs['headers'] = headers
        
        response = self.session.request(method, url, **kwargs)
        
        # Check rate limit headers
        if 'X-RateLimit-Remaining' in response.headers:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            if remaining < 10:
                print(f"Warning: Rate limit approaching ({remaining} remaining)")
        
        return response

# Usage
client = RateLimitedClient('your_api_key')
response = client.make_request('GET', 'https://api.rowellinfra.com/api/v1/accounts')
"""
            }
        }
    
    @staticmethod
    def get_implementation_examples() -> Dict[str, Any]:
        """Get implementation examples for different scenarios"""
        return {
            "exponential_backoff": {
                "title": "Exponential Backoff Implementation",
                "description": "Implement exponential backoff for handling rate limits",
                "javascript": """
async function makeRequestWithBackoff(url, options = {}, maxRetries = 3) {
  let delay = 1000; // Start with 1 second
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, options);
      
      if (response.status === 429) {
        if (attempt === maxRetries) {
          throw new Error('Max retries exceeded');
        }
        
        const retryAfter = response.headers.get('Retry-After');
        delay = retryAfter ? parseInt(retryAfter) * 1000 : delay;
        
        console.log(`Rate limited. Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
        delay *= 2; // Exponential backoff
        continue;
      }
      
      return response;
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }
      
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2;
    }
  }
}
""",
                "python": """
import time
import random
from functools import wraps

def exponential_backoff(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_retries:
                        # Add jitter to prevent thundering herd
                        jitter = random.uniform(0.1, 0.3) * delay
                        sleep_time = min(delay + jitter, max_delay)
                        
                        print(f"Rate limited. Retrying in {sleep_time:.2f}s...")
                        time.sleep(sleep_time)
                        delay *= 2
                        continue
                    raise
            return None
        return wrapper
    return decorator

@exponential_backoff()
def make_api_request(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response
"""
            },
            "request_batching": {
                "title": "Request Batching",
                "description": "Batch multiple requests to reduce rate limit usage",
                "javascript": """
class RequestBatcher {
  constructor(apiKey, batchSize = 10, batchDelay = 1000) {
    this.apiKey = apiKey;
    this.batchSize = batchSize;
    this.batchDelay = batchDelay;
    this.queue = [];
    this.processing = false;
  }
  
  async addRequest(url, options = {}) {
    return new Promise((resolve, reject) => {
      this.queue.push({ url, options, resolve, reject });
      this.processQueue();
    });
  }
  
  async processQueue() {
    if (this.processing || this.queue.length === 0) return;
    
    this.processing = true;
    
    while (this.queue.length > 0) {
      const batch = this.queue.splice(0, this.batchSize);
      
      try {
        const promises = batch.map(({ url, options }) => 
          fetch(url, {
            ...options,
            headers: {
              ...options.headers,
              'X-API-Key': this.apiKey
            }
          })
        );
        
        const responses = await Promise.all(promises);
        
        batch.forEach(({ resolve }, index) => {
          resolve(responses[index]);
        });
        
        if (this.queue.length > 0) {
          await new Promise(resolve => setTimeout(resolve, this.batchDelay));
        }
      } catch (error) {
        batch.forEach(({ reject }) => reject(error));
      }
    }
    
    this.processing = false;
  }
}

// Usage
const batcher = new RequestBatcher('your_api_key');
const responses = await Promise.all([
  batcher.addRequest('/api/v1/accounts/1'),
  batcher.addRequest('/api/v1/accounts/2'),
  batcher.addRequest('/api/v1/accounts/3')
]);
"""
            }
        }
    
    @staticmethod
    def get_monitoring_recommendations() -> Dict[str, Any]:
        """Get monitoring and alerting recommendations"""
        return {
            "metrics_to_track": [
                "Requests per minute/hour/day",
                "Rate limit utilization percentage",
                "429 error frequency",
                "Average response time",
                "API key usage patterns"
            ],
            "alert_thresholds": {
                "warning": "80% of rate limit reached",
                "critical": "95% of rate limit reached",
                "error": "429 responses occurring frequently"
            },
            "monitoring_tools": [
                "Application performance monitoring (APM)",
                "Custom dashboards with rate limit metrics",
                "Log aggregation and analysis",
                "Real-time alerting systems"
            ],
            "dashboard_example": {
                "title": "Rate Limit Dashboard Metrics",
                "widgets": [
                    "Current requests per minute",
                    "Rate limit remaining percentage",
                    "429 error rate over time",
                    "Top endpoints by request volume",
                    "API key usage distribution"
                ]
            }
        }
