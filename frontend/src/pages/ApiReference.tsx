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
  ExternalLink
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Link } from "react-router-dom";
import { CodePlayground } from "@/components/CodePlayground";
import { DashboardLayout } from "@/components/DashboardLayout";

const ApiReference = () => {
  const { toast } = useToast();
  const [selectedEndpoint, setSelectedEndpoint] = useState("register");

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied to clipboard",
      description: "Code has been copied to your clipboard",
    });
  };

  const endpoints = [
    {
      id: "register",
      method: "POST",
      path: "/api/v1/developers/register",
      title: "Developer Registration",
      description: "Register a new developer account",
      category: "Authentication"
    },
    {
      id: "quickstart",
      method: "POST", 
      path: "/api/v1/developers/quickstart",
      title: "Quickstart",
      description: "Complete developer onboarding flow",
      category: "Authentication"
    },
    {
      id: "login",
      method: "GET",
      path: "/api/v1/developers/by-email/{email}",
      title: "Developer Login",
      description: "Get developer by email for login",
      category: "Authentication"
    },
    {
      id: "create-account",
      method: "POST",
      path: "/api/v1/accounts/create",
      title: "Create Account",
      description: "Create a REAL blockchain account on Hedera testnet or Stellar network",
      category: "Accounts",
      isRealBlockchain: true
    },
    {
      id: "list-accounts",
      method: "GET",
      path: "/api/v1/accounts/",
      title: "List Accounts",
      description: "Get all accounts for a project",
      category: "Accounts"
    },
    {
      id: "create-transfer",
      method: "POST",
      path: "/api/v1/transfers/create",
      title: "Create Transfer",
      description: "Create a new transfer transaction",
      category: "Transfers"
    },
    {
      id: "list-transfers",
      method: "GET",
      path: "/api/v1/transfers/",
      title: "List Transfers",
      description: "Get all transfers for a project",
      category: "Transfers"
    }
  ];

  const getEndpointCode = (endpointId: string) => {
    const codes = {
      register: `curl -X POST "http://localhost:8000/api/v1/developers/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "developer@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Acme Corp",
    "role": "developer",
    "country_code": "NG",
    "phone": "+2341234567890"
  }'`,

      quickstart: `curl -X POST "http://localhost:8000/api/v1/developers/quickstart" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "developer@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Acme Corp",
    "role": "developer",
    "country_code": "NG",
    "phone": "+2341234567890",
    "project_name": "My Fintech App",
    "project_description": "A revolutionary fintech application"
  }'`,

      login: `curl -X GET "http://localhost:8000/api/v1/developers/by-email/developer@example.com"`,

      "create-account": `curl -X POST "http://localhost:8000/api/v1/accounts/create" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "network": "hedera",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG"
  }'`,

      "list-accounts": `curl -X GET "http://localhost:8000/api/v1/accounts/" \\
  -H "Authorization: Bearer YOUR_API_KEY"`,

      "create-transfer": `curl -X POST "http://localhost:8000/api/v1/transfers/create" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "from_account": "0.0.740063450",
    "to_account": "0.0.1000001",
    "asset_code": "HBAR",
    "amount": "10.00",
    "network": "hedera",
    "environment": "testnet",
    "from_country": "NG",
    "to_country": "KE"
  }'`,

      "list-transfers": `curl -X GET "http://localhost:8000/api/v1/transfers/" \\
  -H "Authorization: Bearer YOUR_API_KEY"`
    };

    return codes[endpointId] || "";
  };

  const getEndpointResponse = (endpointId: string) => {
    const responses = {
      register: `{
  "id": "cb0dbf2a-d61f-4c5a-8b9e-123456789abc",
  "email": "developer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Acme Corp",
  "role": "developer",
  "country_code": "NG",
  "phone": "+2341234567890",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-09-15T11:00:15Z"
}`,

      quickstart: `{
  "developer": {
    "id": "cb0dbf2a-d61f-4c5a-8b9e-123456789abc",
    "email": "developer@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Acme Corp",
    "role": "developer",
    "country_code": "NG",
    "phone": "+2341234567890",
    "is_active": true,
    "is_verified": false,
    "created_at": "2025-09-15T11:00:15Z"
  },
  "project": {
    "id": "proj_123456789",
    "name": "My Fintech App",
    "description": "A revolutionary fintech application",
    "developer_id": "cb0dbf2a-d61f-4c5a-8b9e-123456789abc",
    "is_active": true,
    "created_at": "2025-09-15T11:00:15Z"
  },
  "api_key": {
    "id": "key_123456789",
    "key_prefix": "ri_GPu9zJuP_",
    "full_key": "ri_GPu9zJuP_9pAhaXPgU8TcmYA_NFVNj_unPv2Ki7fpYc",
    "project_id": "proj_123456789",
    "permissions": ["accounts:read", "accounts:write", "transfers:read", "transfers:write"],
    "is_active": true,
    "created_at": "2025-09-15T11:00:15Z"
  }
}`,

      login: `{
  "id": "cb0dbf2a-d61f-4c5a-8b9e-123456789abc",
  "email": "developer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Acme Corp",
  "role": "developer",
  "country_code": "NG",
  "phone": "+2341234567890",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-09-15T11:00:15Z"
}`,

      "create-account": `{
  "id": "c951627d-0a9e-4010-aa17-5de0ee4cf4f0",
  "account_id": "0.0.12345678",
  "network": "hedera",
  "environment": "testnet",
  "account_type": "user",
  "country_code": "NG",
  "region": null,
  "is_active": true,
  "is_verified": false,
  "is_compliant": false,
  "kyc_status": "pending",
  "key_retrieval_token": "tok_abc123xyz789",
  "key_retrieval_url": "/api/v1/accounts/0.0.12345678/key",
  "metadata": {},
  "created_at": "2025-09-15T11:31:42Z"
}

Note: This is a REAL account on Hedera testnet blockchain.
Verify on HashScan: https://hashscan.io/testnet/account/0.0.12345678`,

      "list-accounts": `[
  {
    "id": "c951627d-0a9e-4010-aa17-5de0ee4cf4f0",
    "account_id": "GBCXGH52IEKJM6KIQ7KDG77KVXQYAFLSUXCZLOPXGPHVW7FXQA4MD35X",
    "network": "stellar",
    "environment": "testnet",
    "account_type": "user",
    "country_code": "NG",
    "is_active": true,
    "is_verified": false,
    "is_compliant": false,
    "kyc_status": "pending",
    "metadata": {},
    "created_at": "2025-09-15T11:31:42Z"
  }
]`,

      "create-transfer": `{
  "id": "a0dbcfc3-1990-4555-b5cd-0a4e5be42a40",
  "transaction_hash": "mock_stellar_tx_-7965415112407877440",
  "network": "stellar",
  "environment": "testnet",
  "transaction_type": "payment",
  "status": "pending",
  "from_account": "GBCXGH52IEKJM6KIQ7KDG77KVXQYAFLSUXCZLOPXGPHVW7FXQA4MD35X",
  "to_account": "GCO6TOYHBYDBKZ3UDAEFWLMB7WXBTBKF7HELCR",
  "asset_code": "XLM",
  "amount": "10.0",
  "memo": "Test transfer",
  "created_at": "2025-09-15T11:31:42Z"
}`,

      "list-transfers": `[
  {
    "id": "a0dbcfc3-1990-4555-b5cd-0a4e5be42a40",
    "transaction_hash": "mock_stellar_tx_-7965415112407877440",
    "network": "stellar",
    "environment": "testnet",
    "transaction_type": "payment",
    "status": "pending",
    "from_account": "GBCXGH52IEKJM6KIQ7KDG77KVXQYAFLSUXCZLOPXGPHVW7FXQA4MD35X",
    "to_account": "GCO6TOYHBYDBKZ3UDAEFWLMB7WXBTBKF7HELCR",
    "asset_code": "XLM",
    "amount": "10.0",
    "memo": "Test transfer",
    "created_at": "2025-09-15T11:31:42Z"
  }
]`
    };

    return responses[endpointId] || "";
  };

  const categories = [...new Set(endpoints.map(ep => ep.category))];

  return (
    <DashboardLayout title="API Reference" description="Complete API documentation for Rowell Infra platform">

      <main className="flex flex-col">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center text-center px-4 sm:px-6 lg:px-8 py-20">
          <div className="absolute inset-0 bg-cover bg-center" style={{backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.8) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuCkQVbCfQvwHWDAIllCKYBnYqWyxPbWPzYFioTOwQEH_CJpc0km4xwTV15HJLlOTly-cNrBA3qcBBq__jCvClQSP6tiHyC8A90JtmAyL8Fu8PGw4BQNlnbboxlVSwweSCjHf7ocZhPGQj1cPvC_zuok9GvXe_lpwfQ6f2l7fVVhHkUAOH0995oniLJuSADxb6wpPgAAvZ6Q_VRUVAEb-g8uRPEBNGQMceVQBehtXGbZS-vZkQp-YXS5rkYoGRoo1xOCYerSCdiT3BNe")'}}></div>
          <div className="relative z-10 max-w-4xl mx-auto flex flex-col items-center gap-6">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight tracking-tighter">API Reference</h1>
            <p className="text-lg sm:text-xl text-gray-200 max-w-2xl">Complete API reference for building African fintech applications with Stellar and Hedera networks</p>
            <Link to="/register">
              <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                <span className="truncate">Get Started</span>
              </Button>
            </Link>
          </div>
        </section>

        {/* Real Blockchain Banner */}
        <section className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 border-b border-green-200 dark:border-green-800">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-center gap-4 p-6 bg-white dark:bg-gray-800 rounded-xl border border-green-200 dark:border-green-800 shadow-sm">
                <div className="flex-shrink-0">
                  <div className="h-12 w-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                    <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                    Real Blockchain Accounts
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    All accounts created via this API are <strong>real accounts on the Hedera testnet blockchain</strong>. 
                    Verify them on{" "}
                    <a 
                      href="https://hashscan.io/testnet" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline font-medium"
                    >
                      HashScan Explorer
                    </a>
                    {" "}and use them for real transactions. No blockchain knowledge required!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* API Info Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">API Information</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Everything you need to know about our API</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                <Globe className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Base URL</h3>
              <code className="text-sm bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">http://localhost:8000</code>
            </div>
            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                <Shield className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Authentication</h3>
              <code className="text-sm bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">Bearer Token</code>
            </div>
            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                <Zap className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Rate Limit</h3>
              <code className="text-sm bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">1000 req/hour</code>
            </div>
            <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                <CheckCircle className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Status</h3>
              <Badge className="bg-green-100 text-green-800">Live</Badge>
            </div>
          </div>
        </section>

        {/* Endpoints Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">API Endpoints</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Explore our comprehensive API endpoints</p>
            </div>

            <div className="grid lg:grid-cols-4 gap-8">
              {/* Sidebar */}
              <div className="lg:col-span-1">
                <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20 sticky top-24">
                  <h3 className="font-semibold mb-4 text-gray-900 dark:text-white">Endpoints</h3>
                  <div className="space-y-2">
                    {categories.map(category => (
                      <div key={category}>
                        <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2 uppercase tracking-wide">
                          {category}
                        </h4>
                        <div className="space-y-1">
                          {endpoints
                            .filter(ep => ep.category === category)
                            .map(endpoint => (
                              <button
                                key={endpoint.id}
                                onClick={() => setSelectedEndpoint(endpoint.id)}
                                className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                                  selectedEndpoint === endpoint.id
                                    ? "bg-primary/10 text-primary"
                                    : "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300"
                                }`}
                              >
                                <div className="flex items-center gap-2">
                                  <Badge 
                                    variant={endpoint.method === "GET" ? "secondary" : "default"}
                                    className={`text-xs ${
                                      endpoint.method === "POST" 
                                        ? "bg-white text-primary border border-primary hover:bg-gray-50" 
                                        : ""
                                    }`}
                                  >
                                    {endpoint.method}
                                  </Badge>
                                  <span className="truncate">{endpoint.title}</span>
                                </div>
                              </button>
                            ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Main Content */}
              <div className="lg:col-span-3">
                {endpoints.map(endpoint => (
                  selectedEndpoint === endpoint.id && (
                    <div key={endpoint.id} className="bg-background-light dark:bg-background-dark p-8 rounded-xl border border-primary/20 dark:border-primary/20">
                      <div className="flex items-center gap-3 mb-6">
                        <Badge 
                          variant={endpoint.method === "GET" ? "secondary" : "default"}
                          className={`text-sm ${
                            endpoint.method === "POST" 
                              ? "bg-white text-primary border border-primary hover:bg-gray-50" 
                              : ""
                          }`}
                        >
                          {endpoint.method}
                        </Badge>
                        <code className="text-lg font-mono text-gray-900 dark:text-white">{endpoint.path}</code>
                      </div>
                      
                      <div className="flex items-center gap-3 mb-2">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{endpoint.title}</h2>
                        {(endpoint as any).isRealBlockchain && (
                          <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 border border-green-300 dark:border-green-700">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Real Blockchain
                          </Badge>
                        )}
                      </div>
                      <p className="text-gray-600 dark:text-gray-300 mb-4">{endpoint.description}</p>
                      {(endpoint as any).isRealBlockchain && (
                        <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                          <div className="flex items-start gap-3">
                            <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
                            <div className="flex-1">
                              <p className="text-sm font-semibold text-green-900 dark:text-green-100 mb-1">
                                ✅ Real Blockchain Account
                              </p>
                              <p className="text-sm text-green-800 dark:text-green-200">
                                Accounts created with this endpoint are <strong>real accounts on the Hedera testnet blockchain</strong>. 
                                You can verify them on{" "}
                                <a 
                                  href={`https://hashscan.io/testnet/account/{account_id}`} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="underline font-medium hover:text-green-600 dark:hover:text-green-300"
                                >
                                  HashScan Explorer
                                </a>.
                                Each account starts with 1 HBAR balance.
                              </p>
                            </div>
                          </div>
                        </div>
                      )}

                      <Tabs defaultValue="request" className="w-full">
                        <TabsList className="grid w-full grid-cols-2">
                          <TabsTrigger value="request">Request</TabsTrigger>
                          <TabsTrigger value="response">Response</TabsTrigger>
                        </TabsList>
                        
                        <TabsContent value="request" className="mt-6">
                          <div className="space-y-4">
                            <div className="flex items-center justify-between">
                              <h3 className="font-semibold text-gray-900 dark:text-white">cURL Example</h3>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => copyToClipboard(getEndpointCode(endpoint.id))}
                              >
                                <Copy className="h-4 w-4 mr-2" />
                                Copy
                              </Button>
                            </div>
                            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto">
                              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
                                {getEndpointCode(endpoint.id)}
                              </pre>
                            </div>
                          </div>
                        </TabsContent>
                        
                        <TabsContent value="response" className="mt-6">
                          <div className="space-y-4">
                            <div className="flex items-center justify-between">
                              <h3 className="font-semibold text-gray-900 dark:text-white">Response Example</h3>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => copyToClipboard(getEndpointResponse(endpoint.id))}
                              >
                                <Copy className="h-4 w-4 mr-2" />
                                Copy
                              </Button>
                            </div>
                            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto">
                              <pre className="text-sm font-mono whitespace-pre-wrap text-gray-900 dark:text-white">
                                {getEndpointResponse(endpoint.id)}
                              </pre>
                            </div>
                          </div>
                        </TabsContent>
                      </Tabs>

                      {/* Interactive Code Playground */}
                      <div className="mt-8">
                        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                          Try It Out
                        </h3>
                        <CodePlayground
                          defaultCode={getEndpointCode(endpoint.id)}
                          apiEndpoint={`http://localhost:8000${endpoint.path}`}
                          method={endpoint.method as "GET" | "POST" | "PUT" | "DELETE"}
                          description={`Test the ${endpoint.title} endpoint directly in your browser`}
                          requiresAuth={endpoint.id !== "register" && endpoint.id !== "quickstart" && endpoint.id !== "login"}
                        />
                      </div>

                      {/* HashScan Verification Link for Account Creation */}
                      {(endpoint as any).isRealBlockchain && endpoint.id === "create-account" && (
                        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                          <div className="flex items-start gap-3">
                            <ExternalLink className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
                            <div className="flex-1">
                              <p className="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-2">
                                🔗 Verify Your Account on Blockchain Explorer
                              </p>
                              <p className="text-sm text-blue-800 dark:text-blue-200 mb-3">
                                After creating an account, verify it's on the real blockchain:
                              </p>
                              <div className="bg-white dark:bg-gray-800 p-3 rounded border border-blue-200 dark:border-blue-700 font-mono text-sm mb-2">
                                <code className="text-blue-900 dark:text-blue-100">
                                  https://hashscan.io/testnet/account/
                                  <span className="text-blue-600 dark:text-blue-400">{`{account_id}`}</span>
                                </code>
                              </div>
                              <p className="text-xs text-blue-700 dark:text-blue-300">
                                Replace <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">{`{account_id}`}</code> with the account_id from the response above
                              </p>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Ready to start building?</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">Get your API key and start building African fintech applications today</p>
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register">
                <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                  <Users className="mr-2 h-5 w-5" />
                  <span className="truncate">Get API Key</span>
                </Button>
              </Link>
              <Link to="/quickstart">
                <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary/20 dark:bg-primary/20 text-primary dark:text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                  <Terminal className="mr-2 h-5 w-5" />
                  <span className="truncate">Quickstart Guide</span>
                </Button>
              </Link>
            </div>
          </div>
        </section>
        </main>
    </DashboardLayout>
  );
};

export default ApiReference;
