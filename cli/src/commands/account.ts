import { Command } from 'commander';
import chalk from 'chalk';

export const accountCommand = new Command('account')
  .description('Manage accounts')
  .action(() => {
    console.log(chalk.blue('Account management commands coming soon!'));
  });
