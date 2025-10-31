#!/usr/bin/env node

/**
 * Rowell Infra CLI
 * Command line tool for managing Rowell Infra projects
 */

import { Command } from 'commander';
import chalk from 'chalk';
import { initCommand } from './commands/init';
import { accountCommand } from './commands/account';
import { transferCommand } from './commands/transfer';
import { analyticsCommand } from './commands/analytics';
import { complianceCommand } from './commands/compliance';
import { configCommand } from './commands/config';

const program = new Command();

// CLI metadata
program
  .name('rowell')
  .description('Rowell Infra CLI - Alchemy for Africa (Stellar + Hedera APIs & Analytics)')
  .version('1.0.0');

// Global options
program
  .option('-v, --verbose', 'Enable verbose logging')
  .option('--api-url <url>', 'Rowell Infra API URL', 'http://localhost:8000')
  .option('--api-key <key>', 'Rowell Infra API key');

// Commands
program
  .addCommand(initCommand)
  .addCommand(accountCommand)
  .addCommand(transferCommand)
  .addCommand(analyticsCommand)
  .addCommand(complianceCommand)
  .addCommand(configCommand);

// Error handling
program.exitOverride();

try {
  program.parse();
} catch (error) {
  console.error(chalk.red('Error:'), (error as Error).message);
  process.exit(1);
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error(chalk.red('Unhandled Rejection at:'), promise, chalk.red('reason:'), reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error(chalk.red('Uncaught Exception:'), error);
  process.exit(1);
});
