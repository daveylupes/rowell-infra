import { Command } from 'commander';
import chalk from 'chalk';

export const configCommand = new Command('config')
  .description('Manage configuration')
  .action(() => {
    console.log(chalk.blue('Configuration commands coming soon!'));
  });
