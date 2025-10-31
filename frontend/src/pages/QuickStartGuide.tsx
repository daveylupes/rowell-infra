import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Code, 
  Copy,
  Terminal,
  Globe,
  Shield,
  Zap,
  Users,
  CheckCircle,
  Play,
  Download,
  ExternalLink,
  Info,
  AlertCircle,
  ArrowRight
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Link } from "react-router-dom";
import { CodePlayground } from "@/components/CodePlayground";
import { DashboardLayout } from "@/components/DashboardLayout";

const QuickStartGuide = () => {
  const { toast } = useToast();
  const [activeStep, setActiveStep] = useState(1);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied to clipboard",
      description: "Code has been copied to your clipboard",
    });
  };

  const steps = [
    {
      id: 1,
      title: "Setup Environment",
      description: "Clone and start the Rowell Infra stack",
      icon: Terminal,
      content: (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Info className="h-4 w-4 text-blue-600" />
              <span className="font-medium text-blue-800">Prerequisites</span>
            </div>
            <p className="text-sm text-blue-700">
              Make sure you have Docker, Docker Compose, Git, and curl installed on your system.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">1. Clone and Start</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`git clone https://github.com/rowell-infra/rowell-infra.git
cd rowell-infra
docker-compose up -d`}
              </pre>
            </div>

            <h3 className="font-semibold text-gray-900 dark:text-white">2. Verify It's Working</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`curl http://localhost:8000/health`}
              </pre>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span className="font-medium text-green-800">Expected Response:</span>
              </div>
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded text-sm font-mono text-gray-900 dark:text-white">
{`{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-01T00:00:00Z"
}`}
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 2,
      title: "Create Your First Account",
      description: "Create a blockchain account using our API",
      icon: Users,
      content: (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Info className="h-4 w-4 text-blue-600" />
              <span className="font-medium text-blue-800">Supported Networks</span>
            </div>
            <p className="text-sm text-blue-700">
              Rowell Infra supports both Stellar and Hedera networks with testnet and mainnet environments.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">Create Account</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`curl -X POST "http://localhost:8000/api/v1/accounts/create" \\
  -H "Content-Type: application/json" \\
  -d '{
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "KE"
  }'`}
              </pre>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span className="font-medium text-green-800">Account Types:</span>
              </div>
              <ul className="text-sm text-green-700 space-y-1">
                <li>• <strong>User</strong>: Individual customers</li>
                <li>• <strong>Merchant</strong>: Businesses accepting payments</li>
                <li>• <strong>Anchor</strong>: Financial institutions</li>
                <li>• <strong>NGO</strong>: Non-profit organizations</li>
              </ul>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 3,
      title: "Make Your First Transfer",
      description: "Send money across borders in seconds",
      icon: Zap,
      content: (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Info className="h-4 w-4 text-blue-600" />
              <span className="font-medium text-blue-800">Cross-Border Transfers</span>
            </div>
            <p className="text-sm text-blue-700">
              Send money between African countries with 3-second settlements and low fees.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">Create Transfer</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`curl -X POST "http://localhost:8000/api/v1/transfers/create" \\
  -H "Content-Type: application/json" \\
  -d '{
    "from_account": "your_account_id",
    "to_account": "destination_account_id",
    "asset_code": "XLM",
    "amount": "10.00",
    "network": "stellar",
    "environment": "testnet"
  }'`}
              </pre>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span className="font-medium text-green-800">Supported Countries:</span>
              </div>
              <div className="text-sm text-green-700">
                🇰🇪 Kenya • 🇳🇬 Nigeria • 🇿🇦 South Africa • 🇬🇭 Ghana • 🇺🇬 Uganda • 🇹🇿 Tanzania • 🇪🇹 Ethiopia • 🇪🇬 Egypt
              </div>
            </div>

            <div className="mt-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Check Transfer Status</h3>
              <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`curl -X GET "http://localhost:8000/api/v1/transfers/{transaction_hash}" \\
  -H "X-API-Key: your_api_key_here"`}
                </pre>
              </div>
              <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Info className="h-4 w-4 text-blue-600" />
                  <span className="font-medium text-blue-800">Status Values:</span>
                </div>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• <strong>pending</strong>: Transaction submitted, awaiting confirmation</li>
                  <li>• <strong>success</strong>: Transaction confirmed on blockchain</li>
                  <li>• <strong>failed</strong>: Transaction failed (insufficient balance, invalid account, etc.)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 4,
      title: "Error Handling",
      description: "Handle errors gracefully in your integration",
      icon: AlertCircle,
      content: (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Info className="h-4 w-4 text-blue-600" />
              <span className="font-medium text-blue-800">Error Responses</span>
            </div>
            <p className="text-sm text-blue-700">
              All errors follow a consistent format with error codes and descriptive messages.
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="font-semibold text-gray-900 dark:text-white">Error Response Format</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`{
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Account balance is insufficient for this transfer",
    "details": {
      "account_id": "0.0.1234567",
      "required": "100.00",
      "available": "50.00"
    }
  }
}`}
              </pre>
            </div>

            <h3 className="font-semibold text-gray-900 dark:text-white">Common Error Codes</h3>
            <div className="space-y-2">
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="font-medium text-red-800 mb-1">INSUFFICIENT_BALANCE</div>
                <p className="text-sm text-red-700">Account doesn't have enough funds for the transaction</p>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="font-medium text-red-800 mb-1">INVALID_ACCOUNT</div>
                <p className="text-sm text-red-700">Account ID format is invalid or account doesn't exist</p>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="font-medium text-red-800 mb-1">RATE_LIMIT_EXCEEDED</div>
                <p className="text-sm text-red-700">Too many requests. Wait before retrying</p>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="font-medium text-red-800 mb-1">NETWORK_ERROR</div>
                <p className="text-sm text-red-700">Blockchain network is temporarily unavailable</p>
              </div>
            </div>

            <h3 className="font-semibold text-gray-900 dark:text-white">Error Handling Example</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
{`try {
  const transfer = await client.transfers.create({
    from_account: 'your_account',
    to_account: 'destination_account',
    amount: '100.00',
    asset_code: 'HBAR'
  });
  console.log('Transfer successful:', transfer.transaction_hash);
} catch (error) {
  if (error.code === 'INSUFFICIENT_BALANCE') {
    console.error('Not enough balance. Current:', error.details.available);
    // Handle insufficient balance
  } else if (error.code === 'RATE_LIMIT_EXCEEDED') {
    console.error('Rate limit exceeded. Retry after:', error.retry_after);
    // Implement retry logic
  } else {
    console.error('Transfer failed:', error.message);
    // Handle other errors
  }
}`}
              </pre>
            </div>
          </div>
        </div>
      )
    }
  ];

  const useCases = [
    {
      title: "Cross-Border Remittances",
      description: "Send money between African countries",
      code: `const transfer = await client.transfers.create({
  from_account: 'kenya_user_account',
  to_account: 'nigeria_user_account',
  asset_code: 'USDC',
  amount: '100.00',
  network: 'stellar',
  environment: 'testnet',
  from_country: 'KE',
  to_country: 'NG'
});`
    },
    {
      title: "Merchant Payments",
      description: "Accept payments in your app",
      code: `// Create merchant account
const merchant = await client.accounts.create({
  network: 'hedera',
  environment: 'testnet',
  account_type: 'merchant',
  country_code: 'ZA'
});

// Process payment
const payment = await client.transfers.create({
  from_account: 'customer_account',
  to_account: merchant.account_id,
  asset_code: 'HBAR',
  amount: '50.00',
  network: 'hedera'
});`
    },
    {
      title: "Analytics & Monitoring",
      description: "Track remittance flows and adoption",
      code: `// Get analytics data
const analytics = await client.analytics.getFlows({
  country: 'KE',
  period: '30d',
  network: 'stellar'
});

// Monitor stablecoin adoption
const adoption = await client.analytics.getAdoption({
  asset: 'USDC',
  region: 'africa'
});`
    }
  ];

  return (
    <DashboardLayout title="Quick Start Guide" description="Get up and running with Rowell Infra in 5 minutes">

        {/* Steps Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">5-Minute Setup</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Follow these steps to get started with Rowell Infra</p>
          </div>

          <div className="space-y-8">
            {steps.map((step, index) => (
              <div key={step.id} className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20">
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0">
                    <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center">
                      <step.icon className="h-8 w-8 text-primary" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-4">
                      <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{step.title}</h3>
                      <Badge variant="outline" className="text-primary border-primary">
                        Step {step.id}
                      </Badge>
                    </div>
                    <p className="text-gray-600 dark:text-gray-300 mb-6">{step.description}</p>
                    {step.content}
                    
                    {/* Interactive Playground for Transfer Step */}
                    {step.id === 3 && (
                      <div className="mt-6">
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
                          Try It Out
                        </h3>
                        <CodePlayground
                          defaultCode={`curl -X POST "http://localhost:8000/api/v1/transfers/create" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: your_api_key_here" \\
  -d '{
    "from_account": "your_account_id",
    "to_account": "destination_account_id",
    "asset_code": "HBAR",
    "amount": "10.00",
    "network": "hedera",
    "environment": "testnet"
  }'`}
                          apiEndpoint="http://localhost:8000/api/v1/transfers/create"
                          method="POST"
                          description="Test the transfer creation endpoint directly in your browser"
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Use Cases Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Common Use Cases</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">See how developers are building with Rowell Infra</p>
            </div>

            <div className="space-y-8">
              {useCases.map((useCase, index) => (
                <div key={index} className="bg-background-light dark:bg-background-dark p-8 rounded-xl border border-primary/20 dark:border-primary/20">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{useCase.title}</h3>
                      <p className="text-gray-600 dark:text-gray-300">{useCase.description}</p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => copyToClipboard(useCase.code)}
                    >
                      <Copy className="h-4 w-4 mr-2" />
                      Copy
                    </Button>
                  </div>
                  <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
                      {useCase.code}
                    </pre>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Resources Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Additional Resources</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Everything you need to build with Rowell Infra</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Code className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">API Reference</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Complete API endpoint documentation</p>
              <Link to="/api-reference">
                <Button variant="outline" size="sm" className="w-full">View Reference</Button>
              </Link>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Terminal className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Interactive Docs</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Try our API directly in your browser</p>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full"
                onClick={() => window.open('http://localhost:8000/docs', '_blank')}
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                Open Docs
              </Button>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Users className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Community</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Join our developer community</p>
              <Link to="/support">
                <Button variant="outline" size="sm" className="w-full">Get Support</Button>
              </Link>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Ready to start building?</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">Join thousands of developers building the future of African payments with Rowell Infra.</p>
              <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/register">
                  <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                    <span className="truncate">Start Building</span>
                  </Button>
                </Link>
                <Link to="/api-reference">
                  <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary/20 dark:bg-primary/20 text-primary dark:text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                    <span className="truncate">View API Reference</span>
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
    </DashboardLayout>
  );
};

export default QuickStartGuide;