import { Command } from 'commander';
import chalk from 'chalk';

export const analyticsCommand = new Command('analytics')
  .description('View analytics and reports')
  .action(() => {
    console.log(chalk.blue('Analytics commands coming soon!'));
  });
