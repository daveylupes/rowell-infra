import axios, { AxiosInstance, AxiosError } from 'axios';
import { AccountService } from './services/account';
import { TransferService } from './services/transfer';
import { AnalyticsService } from './services/analytics';
import { ComplianceService } from './services/compliance';
import { RowellConfig, RowellError } from './types';

// Retry configuration
export interface RetryConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  backoffFactor: number;
  retryCondition?: (error: AxiosError) => boolean;
}

// Default retry configuration
const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 30000,
  backoffFactor: 2,
  retryCondition: (error: AxiosError) => {
    // Retry on network errors, 5xx server errors, and 429 rate limit errors
    return (
      !error.response || 
      error.response.status >= 500 || 
      error.response.status === 429
    );
  }
};

/**
 * Main Rowell Infra client
 */
export class RowellClient {
  private httpClient: AxiosInstance;
  private retryConfig: RetryConfig;
  private enableLogging: boolean;
  public accounts: AccountService;
  public transfers: TransferService;
  public analytics: AnalyticsService;
  public compliance: ComplianceService;

  constructor(config: RowellConfig) {
    // Validate configuration
    this.validateConfig(config);

    // Set retry configuration
    this.retryConfig = {
      ...DEFAULT_RETRY_CONFIG,
      ...config.retry
    };

    // Set logging configuration
    this.enableLogging = config.enableLogging ?? true;

    // Create HTTP client
    this.httpClient = axios.create({
      baseURL: config.baseUrl,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Rowell-Infra-SDK-JS/1.0.0',
        ...config.headers
      }
    });

    // Add API key if provided
    if (config.apiKey) {
      this.httpClient.defaults.headers.common['X-API-Key'] = config.apiKey;
    }

    // Add request interceptor for logging
    this.httpClient.interceptors.request.use(
      (config) => {
        if (this.enableLogging) {
          console.debug('Rowell API Request:', {
            method: config.method?.toUpperCase(),
            url: config.url,
            data: config.data
          });
        }
        return config;
      },
      (error) => {
        if (this.enableLogging) {
          console.error('Rowell API Request Error:', error);
        }
        return Promise.reject(this.createRowellError(error));
      }
    );

    // Add response interceptor for error handling and retry logic
    this.httpClient.interceptors.response.use(
      (response) => {
        if (this.enableLogging) {
          console.debug('Rowell API Response:', {
            status: response.status,
            url: response.config.url,
            data: response.data
          });
        }
        return response;
      },
      async (error: AxiosError) => {
        if (this.enableLogging) {
          console.error('Rowell API Response Error:', {
            status: error.response?.status,
            url: error.config?.url,
            message: error.message,
            data: error.response?.data
          });
        }

        // Check if we should retry
        if (this.shouldRetry(error)) {
          const retryDelay = this.calculateRetryDelay(error);
          if (this.enableLogging) {
            console.debug(`Retrying request in ${retryDelay}ms...`);
          }
          await this.sleep(retryDelay);
          return this.httpClient.request(error.config!);
        }

        return Promise.reject(this.createRowellError(error));
      }
    );

    // Initialize services
    this.accounts = new AccountService(this.httpClient);
    this.transfers = new TransferService(this.httpClient);
    this.analytics = new AnalyticsService(this.httpClient);
    this.compliance = new ComplianceService(this.httpClient);
  }

  /**
   * Validate client configuration
   */
  private validateConfig(config: RowellConfig): void {
    if (!config.baseUrl) {
      throw new Error('baseUrl is required');
    }

    if (!config.baseUrl.startsWith('http://') && !config.baseUrl.startsWith('https://')) {
      throw new Error('baseUrl must start with http:// or https://');
    }

    if (config.timeout && (config.timeout < 1000 || config.timeout > 300000)) {
      throw new Error('timeout must be between 1000ms and 300000ms');
    }
  }

  /**
   * Check if we should retry the request
   */
  private shouldRetry(error: AxiosError): boolean {
    // Check if retry condition is met
    if (!this.retryConfig.retryCondition || !this.retryConfig.retryCondition(error)) {
      return false;
    }

    // Check if we have retry attempts left
    const retryCount = (error.config as any)?.['__retryCount'] || 0;
    return retryCount < this.retryConfig.maxRetries;
  }

  /**
   * Calculate retry delay with exponential backoff
   */
  private calculateRetryDelay(error: AxiosError): number {
    const retryCount = (error.config as any)?.['__retryCount'] || 0;
    
    // Handle rate limiting with special delay
    if (error.response?.status === 429) {
      const retryAfter = error.response.headers['retry-after'];
      if (retryAfter) {
        return parseInt(retryAfter) * 1000;
      }
    }

    // Exponential backoff with jitter
    const delay = Math.min(
      this.retryConfig.baseDelay * Math.pow(this.retryConfig.backoffFactor, retryCount),
      this.retryConfig.maxDelay
    );
    
    // Add jitter to prevent thundering herd
    const jitter = Math.random() * 0.1 * delay;
    return delay + jitter;
  }

  /**
   * Sleep for specified milliseconds
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Create standardized Rowell error
   */
  private createRowellError(error: AxiosError): RowellError {
    const rowellError: RowellError = {
      message: error.message || 'Unknown error occurred',
      timestamp: new Date().toISOString()
    };

    if (error.response) {
      // Server responded with error status
      const responseData = error.response.data as any;
      rowellError.code = responseData?.code || `HTTP_${error.response.status}`;
      rowellError.details = {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      };
    } else if (error.request) {
      // Request was made but no response received
      rowellError.code = 'NETWORK_ERROR';
      rowellError.details = {
        message: 'Network error - no response received'
      };
    } else {
      // Something else happened
      rowellError.code = 'REQUEST_ERROR';
      rowellError.details = {
        message: 'Request setup error'
      };
    }

    return rowellError;
  }

  /**
   * Get API health status
   */
  async getHealth(): Promise<{ status: string; version: string; timestamp: string }> {
    const response = await this.httpClient.get('/health');
    return response.data;
  }

  /**
   * Get API information
   */
  async getInfo(): Promise<{
    name: string;
    description: string;
    version: string;
    docs: string;
    health: string;
    networks: {
      stellar: { testnet: string; mainnet: string };
      hedera: { testnet: string; mainnet: string };
    };
  }> {
    const response = await this.httpClient.get('/');
    return response.data;
  }

  /**
   * Set API key for authentication
   */
  setApiKey(apiKey: string): void {
    this.httpClient.defaults.headers.common['X-API-Key'] = apiKey;
  }

  /**
   * Remove API key
   */
  removeApiKey(): void {
    delete this.httpClient.defaults.headers.common['X-API-Key'];
  }

  /**
   * Set custom headers
   */
  setHeaders(headers: Record<string, string>): void {
    Object.assign(this.httpClient.defaults.headers.common, headers);
  }

  /**
   * Get the underlying HTTP client for advanced usage
   */
  getHttpClient(): AxiosInstance {
    return this.httpClient;
  }

  /**
   * Update retry configuration
   */
  updateRetryConfig(config: Partial<RetryConfig>): void {
    this.retryConfig = { ...this.retryConfig, ...config };
  }

  /**
   * Enable or disable logging
   */
  setLogging(enabled: boolean): void {
    this.enableLogging = enabled;
  }

  /**
   * Get current retry configuration
   */
  getRetryConfig(): RetryConfig {
    return { ...this.retryConfig };
  }

  /**
   * Test API connectivity
   */
  async testConnection(): Promise<boolean> {
    try {
      await this.getHealth();
      return true;
    } catch (error) {
      return false;
    }
  }
}
