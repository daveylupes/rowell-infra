import { Command } from 'commander';
import chalk from 'chalk';

export const complianceCommand = new Command('compliance')
  .description('Manage compliance and KYC')
  .action(() => {
    console.log(chalk.blue('Compliance commands coming soon!'));
  });
