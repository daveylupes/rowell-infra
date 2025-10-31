/**
 * Interactive Code Playground Component
 * Allows developers to test API calls directly in the browser
 */

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Play, 
  Copy, 
  Download, 
  CheckCircle2, 
  AlertCircle, 
  Loader2,
  RefreshCw,
  Key,
  Eye,
  EyeOff
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface CodePlaygroundProps {
  defaultCode?: string;
  apiEndpoint?: string;
  method?: "GET" | "POST" | "PUT" | "DELETE";
  apiKey?: string;
  description?: string;
  requiresAuth?: boolean;
}

export function CodePlayground({
  defaultCode = "",
  apiEndpoint = "/api/v1/accounts",
  method = "GET",
  apiKey: propApiKey = "",
  description = "Test this API endpoint directly",
  requiresAuth = true,
}: CodePlaygroundProps) {
  const { toast } = useToast();
  const [inputApiKey, setInputApiKey] = useState(() => {
    // Load from localStorage or use prop
    const stored = localStorage.getItem('rowell_api_key');
    return stored || propApiKey || '';
  });
  const [showApiKey, setShowApiKey] = useState(false);
  const [code, setCode] = useState(defaultCode);
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);

  // Save API key to localStorage when changed
  useEffect(() => {
    if (inputApiKey) {
      localStorage.setItem('rowell_api_key', inputApiKey);
    }
  }, [inputApiKey]);

  // Update code with API key when it changes
  useEffect(() => {
    if (inputApiKey && defaultCode && requiresAuth) {
      // Replace placeholder API key in code (case-insensitive)
      const updatedCode = defaultCode.replace(
        /YOUR_API_KEY|ri_your_api_key_here|ri_abc123xyz789|Bearer\s+ri_[^\s'"]*/gi,
        inputApiKey
      );
      setCode(updatedCode);
    } else if (!inputApiKey && defaultCode && requiresAuth) {
      // Reset to default if API key is removed
      setCode(defaultCode);
    }
  }, [inputApiKey, defaultCode, requiresAuth]);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied to clipboard",
      description: "Code has been copied to your clipboard",
    });
  };

  const handleDownload = (content: string, filename: string) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast({
      title: "Downloaded",
      description: `${filename} has been downloaded`,
    });
  };

  const executeCode = async () => {
    setLoading(true);
    setError(null);
    setResponse("");
    setResponseTime(null);

    try {
      const startTime = performance.now();

      // Parse the code to extract API call details
      // This is a simplified version - in production, use a proper parser
      const apiUrl = apiEndpoint || "http://localhost:8000/api/v1/accounts";
      
      // Get API key from input (prefer inputApiKey over prop)
      const actualApiKey = inputApiKey || propApiKey;
      
      if (requiresAuth && !actualApiKey) {
        throw new Error("API key is required. Please enter your API key above.");
      }

      // Parse request body from code
      let requestBody: string | undefined;
      if (method !== "GET" && code) {
        try {
          // Try to extract JSON from curl command or direct JSON
          const jsonMatch = code.match(/\{[\s\S]*?\}/);
          if (jsonMatch) {
            requestBody = jsonMatch[0];
          }
        } catch (e) {
          // Not JSON, skip body
        }
      }

      // Build headers with API key
      const headers: HeadersInit = {
        "Content-Type": "application/json",
      };

      if (actualApiKey) {
        headers["Authorization"] = `Bearer ${actualApiKey}`;
      }

      const fetchOptions: RequestInit = {
        method,
        headers,
        ...(requestBody ? { body: requestBody } : {}),
      };

      // Make actual API call
      const res = await fetch(apiUrl, fetchOptions);
      const endTime = performance.now();
      setResponseTime(Math.round(endTime - startTime));

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));

      if (!res.ok) {
        setError(`API Error: ${res.status} ${res.statusText}`);
      }
    } catch (err: any) {
      setError(err.message || "Failed to execute code");
      setResponse("");
    } finally {
      setLoading(false);
    }
  };

  const clearOutput = () => {
    setResponse("");
    setError(null);
    setResponseTime(null);
  };

  const getJavaScriptCode = () => {
    const actualApiKey = inputApiKey || propApiKey || 'YOUR_API_KEY';
    const apiUrl = apiEndpoint || "http://localhost:8000/api/v1/accounts";
    
    if (method === "GET") {
      return `// JavaScript Example
const apiKey = "${actualApiKey}";
const response = await fetch("${apiUrl}", {
  method: "${method}",
  headers: {
    "Authorization": \`Bearer \${apiKey}\`,
    "Content-Type": "application/json"
  }
});

const data = await response.json();
console.log(data);`;
    } else {
      // Extract JSON body from curl command
      const jsonMatch = code.match(/\{[\s\S]*?\}/);
      const bodyJson = jsonMatch ? jsonMatch[0] : '{}';
      
      return `// JavaScript Example
const apiKey = "${actualApiKey}";
const response = await fetch("${apiUrl}", {
  method: "${method}",
  headers: {
    "Authorization": \`Bearer \${apiKey}\`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(${bodyJson})
});

const data = await response.json();
console.log(data);`;
    }
  };

  return (
    <Card className="w-full">
      <div className="p-6 space-y-4">
        {description && (
          <p className="text-sm text-muted-foreground">{description}</p>
        )}

        {/* API Key Input */}
        {requiresAuth && (
          <div className="space-y-2 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <div className="flex items-center gap-2">
              <Key className="h-4 w-4 text-blue-600 dark:text-blue-400" />
              <Label htmlFor="api-key-input" className="text-sm font-semibold text-blue-900 dark:text-blue-100">
                Your API Key
              </Label>
            </div>
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <Input
                  id="api-key-input"
                  type={showApiKey ? "text" : "password"}
                  placeholder="ri_..."
                  value={inputApiKey}
                  onChange={(e) => setInputApiKey(e.target.value)}
                  className="font-mono text-sm pr-10"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7 p-0"
                  onClick={() => setShowApiKey(!showApiKey)}
                >
                  {showApiKey ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </Button>
              </div>
              {inputApiKey && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    navigator.clipboard.writeText(inputApiKey);
                    toast({
                      title: "Copied!",
                      description: "API key copied to clipboard",
                    });
                  }}
                >
                  <Copy className="h-4 w-4" />
                </Button>
              )}
            </div>
            <p className="text-xs text-blue-700 dark:text-blue-300">
              💡 Enter your API key to test endpoints. Get one from{" "}
              <a href="/developer-dashboard" className="underline font-medium">Developer Dashboard</a>
            </p>
          </div>
        )}

        <Tabs defaultValue="curl" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="curl">cURL</TabsTrigger>
            <TabsTrigger value="javascript">JavaScript</TabsTrigger>
            <TabsTrigger value="response">
              Response
              {responseTime !== null && (
                <Badge variant="secondary" className="ml-2">
                  {responseTime}ms
                </Badge>
              )}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="curl" className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>cURL Command</Label>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleCopy(code)}
                  >
                    <Copy className="h-4 w-4 mr-2" />
                    Copy
                  </Button>
                </div>
              </div>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="cURL command will appear here..."
                className="flex min-h-[200px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm font-mono ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span>Method: {method}</span>
                <span>•</span>
                <span>Endpoint: {apiEndpoint}</span>
              </div>
              <Button
                onClick={executeCode}
                disabled={loading || !code.trim() || (requiresAuth && !inputApiKey && !propApiKey)}
                className="flex items-center gap-2 bg-gradient-to-r from-accent-start to-accent-end text-white"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Run Request
                  </>
                )}
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="javascript" className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>JavaScript Example</Label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const jsCode = getJavaScriptCode();
                    handleCopy(jsCode);
                  }}
                >
                  <Copy className="h-4 w-4 mr-2" />
                  Copy
                </Button>
              </div>
              <pre className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-auto text-sm font-mono text-gray-900 dark:text-white">
                {getJavaScriptCode()}
              </pre>
            </div>
            <p className="text-xs text-muted-foreground">
              This JavaScript code shows how to call the API from a browser or Node.js application.
            </p>
          </TabsContent>

          <TabsContent value="response" className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Response</Label>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={clearOutput}
                    disabled={!response && !error}
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Clear
                  </Button>
                  {response && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCopy(response)}
                    >
                      <Copy className="h-4 w-4 mr-2" />
                      Copy
                    </Button>
                  )}
                </div>
              </div>

              {error ? (
                <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                  <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
                    <AlertCircle className="h-4 w-4" />
                    <span className="font-medium">Error</span>
                  </div>
                  <p className="mt-2 text-sm text-red-700 dark:text-red-300">
                    {error}
                  </p>
                </div>
              ) : response ? (
                <div className="relative">
                  <pre className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-auto text-sm font-mono text-gray-900 dark:text-white">
                    {response}
                  </pre>
                  {responseTime !== null && (
                    <div className="absolute top-2 right-2">
                      <Badge variant="secondary">
                        {responseTime}ms
                      </Badge>
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-8 text-center text-muted-foreground border-2 border-dashed rounded-lg">
                  <p>No response yet. Run the code to see results.</p>
                </div>
              )}
            </div>

            {response && !error && (
              <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400">
                <CheckCircle2 className="h-4 w-4" />
                <span>Request completed successfully</span>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </Card>
  );
}


