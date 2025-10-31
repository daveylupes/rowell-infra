import { Command } from 'commander';
import inquirer from 'inquirer';
import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs-extra';
import path from 'path';

export const initCommand = new Command('init')
  .description('Initialize a new Rowell Infra project')
  .option('-d, --directory <dir>', 'Project directory', '.')
  .option('--skip-questions', 'Skip interactive questions and use defaults')
  .action(async (options) => {
    try {
      console.log(chalk.blue.bold('\n🚀 Rowell Infra Project Initialization\n'));
      
      const projectDir = path.resolve(options.directory);
      
      // Check if directory exists and is empty
      if (await fs.pathExists(projectDir)) {
        const files = await fs.readdir(projectDir);
        if (files.length > 0 && !options.skipQuestions) {
          const { proceed } = await inquirer.prompt([
            {
              type: 'confirm',
              name: 'proceed',
              message: `Directory ${projectDir} is not empty. Continue anyway?`,
              default: false
            }
          ]);
          
          if (!proceed) {
            console.log(chalk.yellow('Initialization cancelled.'));
            return;
          }
        }
      }
      
      // Create project directory
      await fs.ensureDir(projectDir);
      
      // Get project configuration
      let config: any = {};
      
      if (!options.skipQuestions) {
        const answers = await inquirer.prompt([
          {
            type: 'input',
            name: 'projectName',
            message: 'Project name:',
            default: path.basename(projectDir),
            validate: (input) => input.length > 0 || 'Project name is required'
          },
          {
            type: 'input',
            name: 'description',
            message: 'Project description:',
            default: 'Rowell Infra project for African fintech'
          },
          {
            type: 'list',
            name: 'network',
            message: 'Primary network:',
            choices: [
              { name: 'Stellar', value: 'stellar' },
              { name: 'Hedera', value: 'hedera' },
              { name: 'Both', value: 'both' }
            ],
            default: 'both'
          },
          {
            type: 'list',
            name: 'environment',
            message: 'Environment:',
            choices: [
              { name: 'Testnet', value: 'testnet' },
              { name: 'Mainnet', value: 'mainnet' }
            ],
            default: 'testnet'
          },
          {
            type: 'list',
            name: 'language',
            message: 'Programming language:',
            choices: [
              { name: 'JavaScript/TypeScript', value: 'js' },
              { name: 'Python', value: 'python' },
              { name: 'Flutter/Dart', value: 'flutter' }
            ],
            default: 'js'
          },
          {
            type: 'input',
            name: 'apiUrl',
            message: 'Rowell Infra API URL:',
            default: 'http://localhost:8000'
          },
          {
            type: 'input',
            name: 'apiKey',
            message: 'API Key (optional):',
            default: ''
          }
        ]);
        
        config = answers;
      } else {
        // Use defaults
        config = {
          projectName: path.basename(projectDir),
          description: 'Rowell Infra project for African fintech',
          network: 'both',
          environment: 'testnet',
          language: 'js',
          apiUrl: 'http://localhost:8000',
          apiKey: ''
        };
      }
      
      const spinner = ora('Creating project files...').start();
      
      try {
        // Create package.json (for JS/TS projects)
        if (config.language === 'js') {
          const packageJson = {
            name: config.projectName,
            version: '1.0.0',
            description: config.description,
            main: 'index.js',
            scripts: {
              start: 'node index.js',
              dev: 'node --watch index.js'
            },
            dependencies: {
              '@rowell-infra/sdk': '^1.0.0'
            },
            keywords: ['rowell-infra', 'stellar', 'hedera', 'africa', 'fintech'],
            author: '',
            license: 'MIT'
          };
          
          await fs.writeJson(path.join(projectDir, 'package.json'), packageJson, { spaces: 2 });
        }
        
        // Create requirements.txt (for Python projects)
        if (config.language === 'python') {
          const requirementsContent = `# Rowell Infra Python SDK
rowell-infra-sdk>=1.0.0

# Additional dependencies
python-dotenv>=1.0.0
requests>=2.31.0
asyncio>=3.4.3
`;
          
          await fs.writeFile(path.join(projectDir, 'requirements.txt'), requirementsContent);
        }
        
        // Create .env file
        const envContent = `# Rowell Infra Configuration
ROWELL_API_URL=${config.apiUrl}
ROWELL_API_KEY=${config.apiKey}
ROWELL_NETWORK=${config.network}
ROWELL_ENVIRONMENT=${config.environment}

# Your project configuration
PROJECT_NAME=${config.projectName}
PROJECT_DESCRIPTION=${config.description}
`;
        
        await fs.writeFile(path.join(projectDir, '.env'), envContent);
        
        // Create .env.example
        const envExampleContent = `# Rowell Infra Configuration
ROWELL_API_URL=http://localhost:8000
ROWELL_API_KEY=your_api_key_here
ROWELL_NETWORK=both
ROWELL_ENVIRONMENT=testnet

# Your project configuration
PROJECT_NAME=my-rowell-project
PROJECT_DESCRIPTION=My Rowell Infra project
`;
        
        await fs.writeFile(path.join(projectDir, '.env.example'), envExampleContent);
        
        // Create .gitignore
        const gitignoreContent = `# Dependencies
node_modules/
*.log
npm-debug.log*

# Environment variables
.env
.env.local
.env.production

# Build outputs
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Rowell Infra specific
.rowell/
secrets/
*.key
*.pem
`;
        
        await fs.writeFile(path.join(projectDir, '.gitignore'), gitignoreContent);
        
        // Create README.md
        const readmeContent = `# ${config.projectName}

${config.description}

## Getting Started

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Configure your environment:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

3. Run the project:
   \`\`\`bash
   npm start
   \`\`\`

## Rowell Infra SDK

This project uses the Rowell Infra SDK to interact with Stellar and Hedera networks.

### Example Usage

\`\`\`javascript
const { RowellClient } = require('@rowell-infra/sdk');

const client = new RowellClient({
  baseUrl: process.env.ROWELL_API_URL,
  apiKey: process.env.ROWELL_API_KEY
});

// Create an account
const account = await client.accounts.create({
  network: 'stellar',
  environment: 'testnet',
  account_type: 'user',
  country_code: 'KE'
});

// Send a transfer
const transfer = await client.transfers.create({
  from_account: 'source_account_id',
  to_account: 'destination_account_id',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet'
});
\`\`\`

## Documentation

- [Rowell Infra Documentation](https://docs.rowell-infra.com)
- [API Reference](https://api.rowell-infra.com/docs)
- [SDK Documentation](https://sdk.rowell-infra.com)

## Support

- [GitHub Issues](https://github.com/rowell-infra/rowell-infra/issues)
- [Discord Community](https://discord.gg/rowell-infra)
- [Email Support](mailto:support@rowell-infra.com)
`;
        
        await fs.writeFile(path.join(projectDir, 'README.md'), readmeContent);
        
        // Create example files based on language
        if (config.language === 'js') {
          const exampleJsContent = `const { RowellClient } = require('@rowell-infra/sdk');
require('dotenv').config();

async function main() {
  // Initialize Rowell client
  const client = new RowellClient({
    baseUrl: process.env.ROWELL_API_URL,
    apiKey: process.env.ROWELL_API_KEY
  });

  try {
    // Check API health
    const health = await client.getHealth();
    console.log('API Health:', health);

    // Create a new account
    console.log('Creating account...');
    const account = await client.accounts.create({
      network: 'stellar',
      environment: 'testnet',
      account_type: 'user',
      country_code: 'KE'
    });
    console.log('Account created:', account);

    // Get account balances
    const balances = await client.accounts.getBalances(account.account_id);
    console.log('Account balances:', balances);

  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
`;
          
          await fs.writeFile(path.join(projectDir, 'index.js'), exampleJsContent);
          
          // Create TypeScript example
          const exampleTsContent = `import { RowellClient } from '@rowell-infra/sdk';
import dotenv from 'dotenv';

dotenv.config();

async function main(): Promise<void> {
  // Initialize Rowell client
  const client = new RowellClient({
    baseUrl: process.env.ROWELL_API_URL!,
    apiKey: process.env.ROWELL_API_KEY
  });

  try {
    // Check API health
    const health = await client.getHealth();
    console.log('API Health:', health);

    // Create a new account
    console.log('Creating account...');
    const account = await client.accounts.create({
      network: 'stellar',
      environment: 'testnet',
      account_type: 'user',
      country_code: 'KE'
    });
    console.log('Account created:', account);

    // Get account balances
    const balances = await client.accounts.getBalances(account.account_id);
    console.log('Account balances:', balances);

  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
`;
          
          await fs.writeFile(path.join(projectDir, 'index.ts'), exampleTsContent);
        }
        
        // Create Python example
        if (config.language === 'python') {
          const examplePyContent = `#!/usr/bin/env python3
"""
Rowell Infra Python Example
Alchemy for Africa: Stellar + Hedera APIs & Analytics
"""

import asyncio
import os
from dotenv import load_dotenv
from rowell_infra import RowellClient

# Load environment variables
load_dotenv()

async def main():
    """Main function demonstrating Rowell Infra Python SDK usage."""
    
    # Initialize Rowell client
    client = RowellClient(
        base_url=os.getenv('ROWELL_API_URL'),
        api_key=os.getenv('ROWELL_API_KEY')
    )
    
    try:
        # Check API health
        health = await client.get_health()
        print(f'API Health: {health}')
        
        # Create a new account
        print('Creating account...')
        account = await client.accounts.create(
            network='stellar',
            environment='testnet',
            account_type='user',
            country_code='KE'
        )
        print(f'Account created: {account}')
        
        # Get account balances
        balances = await client.accounts.get_balances(account.account_id)
        print(f'Account balances: {balances}')
        
    except Exception as error:
        print(f'Error: {error}')

if __name__ == '__main__':
    asyncio.run(main())
`;
          
          await fs.writeFile(path.join(projectDir, 'main.py'), examplePyContent);
          
          // Create setup script for Python virtual environment
          const setupPyContent = `#!/usr/bin/env python3
"""
Setup script for Python virtual environment
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_python_env():
    """Set up Python virtual environment and install dependencies."""
    print("Setting up Python virtual environment...")
    
    # Create virtual environment
    success, output = run_command("python -m venv venv")
    if not success:
        print(f"Error creating virtual environment: {output}")
        return False
    
    print("Virtual environment created successfully!")
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = "venv\\\\Scripts\\\\activate"
        pip_path = "venv\\\\Scripts\\\\pip"
    else:  # Unix/Linux/macOS
        activate_script = "source venv/bin/activate"
        pip_path = "venv/bin/pip"
    
    # Install dependencies
    print("Installing dependencies...")
    success, output = run_command(f"{pip_path} install --upgrade pip")
    if not success:
        print(f"Error upgrading pip: {output}")
        return False
    
    success, output = run_command(f"{pip_path} install -r requirements.txt")
    if not success:
        print(f"Error installing dependencies: {output}")
        return False
    
    print("Dependencies installed successfully!")
    print("")
    print("To activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("  venv\\\\Scripts\\\\activate")
    else:  # Unix/Linux/macOS
        print("  source venv/bin/activate")
    print("")
    print("To run the example:")
    print("  python main.py")
    
    return True

if __name__ == "__main__":
    setup_python_env()
`;
          
          await fs.writeFile(path.join(projectDir, 'setup_env.py'), setupPyContent);
        }
        
        spinner.succeed('Project files created successfully!');
        
        // Show next steps
        console.log(chalk.green.bold('\n✅ Project initialized successfully!\n'));
        console.log(chalk.cyan('Next steps:'));
        console.log(chalk.white('1. cd ' + projectDir));
        
        if (config.language === 'python') {
          console.log(chalk.white('2. python setup_env.py  # Set up virtual environment'));
          console.log(chalk.white('3. source venv/bin/activate  # Activate virtual environment'));
          console.log(chalk.white('4. Edit .env with your configuration'));
          console.log(chalk.white('5. python main.py  # Run the example'));
        } else if (config.language === 'js') {
          console.log(chalk.white('2. npm install'));
          console.log(chalk.white('3. Edit .env with your configuration'));
          console.log(chalk.white('4. npm start'));
        } else if (config.language === 'flutter') {
          console.log(chalk.white('2. flutter pub get'));
          console.log(chalk.white('3. Edit .env with your configuration'));
          console.log(chalk.white('4. flutter run'));
        }
        
        console.log(chalk.white('\nHappy coding! 🚀\n'));
        
      } catch (error) {
        spinner.fail('Failed to create project files');
        throw error;
      }
      
    } catch (error) {
      console.error(chalk.red('Error:'), (error as Error).message);
      process.exit(1);
    }
  });
