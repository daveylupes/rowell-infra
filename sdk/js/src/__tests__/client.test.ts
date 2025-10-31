/**
 * Tests for Rowell Infra JavaScript SDK Client
 */

import { RowellClient, RetryConfig } from '../client';
import { RowellConfig } from '../types';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('RowellClient', () => {
  let client: RowellClient;
  let mockAxiosInstance: any;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create mock axios instance
    mockAxiosInstance = {
      defaults: {
        headers: {
          common: {}
        }
      },
      interceptors: {
        request: {
          use: jest.fn()
        },
        response: {
          use: jest.fn()
        }
      },
      get: jest.fn(),
      post: jest.fn(),
      patch: jest.fn(),
      delete: jest.fn(),
      request: jest.fn()
    };

    // Mock axios.create to return our mock instance
    mockedAxios.create.mockReturnValue(mockAxiosInstance);

    // Create client with test config
    const config: RowellConfig = {
      baseUrl: 'https://api.rowellinfra.com',
      apiKey: 'test-api-key',
      timeout: 30000,
      enableLogging: false
    };

    client = new RowellClient(config);
  });

  describe('constructor', () => {
    it('should create client with valid configuration', () => {
      expect(client).toBeDefined();
      expect(mockedAxios.create).toHaveBeenCalledWith({
        baseURL: 'https://api.rowellinfra.com',
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Rowell-Infra-SDK-JS/1.0.0'
        }
      });
    });

    it('should set API key in headers', () => {
      expect(mockAxiosInstance.defaults.headers.common['X-API-Key']).toBe('test-api-key');
    });

    it('should initialize all services', () => {
      expect(client.accounts).toBeDefined();
      expect(client.transfers).toBeDefined();
      expect(client.analytics).toBeDefined();
      expect(client.compliance).toBeDefined();
    });

    it('should set up request and response interceptors', () => {
      expect(mockAxiosInstance.interceptors.request.use).toHaveBeenCalled();
      expect(mockAxiosInstance.interceptors.response.use).toHaveBeenCalled();
    });
  });

  describe('configuration validation', () => {
    it('should throw error for missing baseUrl', () => {
      expect(() => {
        new RowellClient({} as RowellConfig);
      }).toThrow('baseUrl is required');
    });

    it('should throw error for invalid baseUrl', () => {
      expect(() => {
        new RowellClient({
          baseUrl: 'invalid-url'
        } as RowellConfig);
      }).toThrow('baseUrl must start with http:// or https://');
    });

    it('should throw error for invalid timeout', () => {
      expect(() => {
        new RowellClient({
          baseUrl: 'https://api.rowellinfra.com',
          timeout: 500 // Too low
        });
      }).toThrow('timeout must be between 1000ms and 300000ms');

      expect(() => {
        new RowellClient({
          baseUrl: 'https://api.rowellinfra.com',
          timeout: 400000 // Too high
        });
      }).toThrow('timeout must be between 1000ms and 300000ms');
    });
  });

  describe('API key management', () => {
    it('should set API key', () => {
      client.setApiKey('new-api-key');
      expect(mockAxiosInstance.defaults.headers.common['X-API-Key']).toBe('new-api-key');
    });

    it('should remove API key', () => {
      client.removeApiKey();
      expect(mockAxiosInstance.defaults.headers.common['X-API-Key']).toBeUndefined();
    });
  });

  describe('headers management', () => {
    it('should set custom headers', () => {
      const customHeaders = {
        'Custom-Header': 'custom-value',
        'Another-Header': 'another-value'
      };

      client.setHeaders(customHeaders);

      expect(mockAxiosInstance.defaults.headers.common['Custom-Header']).toBe('custom-value');
      expect(mockAxiosInstance.defaults.headers.common['Another-Header']).toBe('another-value');
    });
  });

  describe('retry configuration', () => {
    it('should update retry configuration', () => {
      const newRetryConfig: Partial<RetryConfig> = {
        maxRetries: 5,
        baseDelay: 2000
      };

      client.updateRetryConfig(newRetryConfig);
      const currentConfig = client.getRetryConfig();

      expect(currentConfig.maxRetries).toBe(5);
      expect(currentConfig.baseDelay).toBe(2000);
      expect(currentConfig.maxDelay).toBe(30000); // Should keep existing value
    });
  });

  describe('logging', () => {
    it('should enable logging', () => {
      client.setLogging(true);
      // Note: We can't easily test the logging behavior without more complex mocking
    });

    it('should disable logging', () => {
      client.setLogging(false);
      // Note: We can't easily test the logging behavior without more complex mocking
    });
  });

  describe('health check', () => {
    it('should get health status', async () => {
      const mockHealthData = {
        status: 'healthy',
        version: '1.0.0',
        timestamp: '2024-01-27T00:00:00Z'
      };

      mockAxiosInstance.get.mockResolvedValue({
        data: mockHealthData
      });

      const result = await client.getHealth();

      expect(result).toEqual(mockHealthData);
      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/health');
    });

    it('should get API info', async () => {
      const mockInfoData = {
        name: 'Rowell Infra API',
        description: 'Alchemy for Africa: Stellar + Hedera APIs & Analytics',
        version: '1.0.0',
        docs: '/docs',
        health: '/health',
        networks: {
          stellar: { testnet: 'testnet', mainnet: 'mainnet' },
          hedera: { testnet: 'testnet', mainnet: 'mainnet' }
        }
      };

      mockAxiosInstance.get.mockResolvedValue({
        data: mockInfoData
      });

      const result = await client.getInfo();

      expect(result).toEqual(mockInfoData);
      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/');
    });
  });

  describe('connection testing', () => {
    it('should return true for successful connection test', async () => {
      mockAxiosInstance.get.mockResolvedValue({
        data: { status: 'healthy' }
      });

      const result = await client.testConnection();

      expect(result).toBe(true);
    });

    it('should return false for failed connection test', async () => {
      mockAxiosInstance.get.mockRejectedValue(new Error('Connection failed'));

      const result = await client.testConnection();

      expect(result).toBe(false);
    });
  });

  describe('HTTP client access', () => {
    it('should return the underlying HTTP client', () => {
      const httpClient = client.getHttpClient();

      expect(httpClient).toBe(mockAxiosInstance);
    });
  });

  describe('retry configuration with custom settings', () => {
    it('should use custom retry configuration', () => {
      const config: RowellConfig = {
        baseUrl: 'https://api.rowellinfra.com',
        retry: {
          maxRetries: 5,
          baseDelay: 2000,
          maxDelay: 60000,
          backoffFactor: 3
        }
      };

      const customClient = new RowellClient(config);
      const retryConfig = customClient.getRetryConfig();

      expect(retryConfig.maxRetries).toBe(5);
      expect(retryConfig.baseDelay).toBe(2000);
      expect(retryConfig.maxDelay).toBe(60000);
      expect(retryConfig.backoffFactor).toBe(3);
    });
  });

  describe('error handling', () => {
    it('should handle network errors gracefully', async () => {
      const networkError = new Error('Network Error');
      mockAxiosInstance.get.mockRejectedValue(networkError);

      await expect(client.getHealth()).rejects.toThrow();
    });

    it('should handle API errors gracefully', async () => {
      const apiError = {
        response: {
          status: 400,
          statusText: 'Bad Request',
          data: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid request parameters'
          }
        },
        message: 'Request failed with status code 400'
      };

      mockAxiosInstance.get.mockRejectedValue(apiError);

      try {
        await client.getHealth();
        fail('Expected error to be thrown');
      } catch (error) {
        expect(error).toBeDefined();
        expect(error.message).toBe('Request failed with status code 400');
      }
    });
  });
});
