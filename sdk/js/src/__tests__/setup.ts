/**
 * Jest test setup file
 */

// Mock console methods to reduce noise in tests
(global as any).console = {
  ...console,
  debug: jest.fn(),
  log: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

// Mock setTimeout and setInterval for testing
(jest as any).useFakeTimers();

// Global test timeout
(jest as any).setTimeout(10000);
