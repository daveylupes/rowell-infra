import { Command } from 'commander';
import chalk from 'chalk';

export const transferCommand = new Command('transfer')
  .description('Manage transfers')
  .action(() => {
    console.log(chalk.blue('Transfer management commands coming soon!'));
  });
