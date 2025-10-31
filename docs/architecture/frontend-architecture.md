# 🎨 Frontend Architecture - Rowell Infra

> **React-based frontend architecture for African fintech infrastructure**

## 📋 Overview

The Rowell Infra frontend is built using **React 18** with **TypeScript**, providing a modern, responsive interface for managing blockchain operations, analytics, and compliance features.

## 🛠️ Technology Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and building
- **UI Library**: Radix UI primitives with Tailwind CSS
- **State Management**: TanStack Query (React Query) for server state
- **Routing**: React Router v6
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts for data visualization
- **Styling**: Tailwind CSS with custom design system

## 🏗️ Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
├─────────────────────────────────────────────────────────────┤
│  Landing Page    Dashboard    Developer Tools              │
│  Account Mgmt    Transfers    Documentation                │
│  Analytics       Compliance   Settings                     │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  Component Layer                            │
├─────────────────────────────────────────────────────────────┤
│  UI Components    Forms      Charts    Tables              │
│  (Radix UI)      (RHF)     (Recharts)  (Custom)           │
│  Layouts         Modals     Cards      Navigation         │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  State Management                           │
├─────────────────────────────────────────────────────────────┤
│  TanStack Query    React Hook Form    Local State          │
│  Server State      Form State         Component State      │
│  Cache Management  Validation         UI State             │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    API Integration                          │
├─────────────────────────────────────────────────────────────┤
│  Custom Hooks      API Client      Error Handling          │
│  use-api.ts        lib/api.ts      Toast Notifications     │
│  Query Hooks       TypeScript      Loading States          │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
frontend/src/
├── components/              # Reusable UI components
│   ├── ui/                 # Radix UI components
│   ├── forms/              # Form components
│   ├── charts/             # Chart components
│   └── layout/             # Layout components
├── pages/                   # Page components
│   ├── Landing.tsx
│   ├── Dashboard.tsx
│   ├── AccountManagement.tsx
│   └── Documentation.tsx
├── hooks/                   # Custom React hooks
│   ├── use-api.ts          # API integration hooks
│   └── use-mobile.tsx      # Mobile detection
├── lib/                     # Utility libraries
│   ├── api.ts              # API client
│   └── utils.ts            # Utility functions
├── types/                   # TypeScript type definitions
└── styles/                  # Global styles and Tailwind config
```

## 🔧 Key Components

### Page Components

| Page | Purpose | Key Features |
|------|---------|--------------|
| **Landing** | Marketing and onboarding | Hero section, features, pricing |
| **Dashboard** | Business analytics | KPIs, charts, recent activity |
| **Developer Dashboard** | Technical metrics | API usage, rate limits, logs |
| **Account Management** | Account operations | Create, list, manage accounts |
| **Transfers** | Transfer operations | Send, track, history |
| **Documentation** | API documentation | Interactive docs, examples |

### Component Examples

```typescript
// Account Management Page
const AccountManagement = () => {
  const { data: accounts, isLoading, error } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => api.accounts.list(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const createAccountMutation = useMutation({
    mutationFn: api.accounts.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      toast.success('Account created successfully');
    },
  });

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Account Management</h1>
        <CreateAccountDialog />
      </div>
      
      {isLoading && <AccountListSkeleton />}
      {error && <ErrorMessage error={error} />}
      {accounts && <AccountList accounts={accounts} />}
    </div>
  );
};
```

## 🔄 State Management

### Server State (TanStack Query)

```typescript
// API hooks
export const useAccounts = () => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: api.accounts.list,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCreateAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.accounts.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    },
  });
};
```

### Form State (React Hook Form)

```typescript
// Form component
const CreateAccountForm = () => {
  const form = useForm<AccountCreateSchema>({
    resolver: zodResolver(accountCreateSchema),
  });

  const createAccount = useCreateAccount();

  const onSubmit = (data: AccountCreateSchema) => {
    createAccount.mutate(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="network"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Network</FormLabel>
              <Select onValueChange={field.onChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select network" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="stellar">Stellar</SelectItem>
                  <SelectItem value="hedera">Hedera</SelectItem>
                </SelectContent>
              </Select>
            </FormItem>
          )}
        />
        <Button type="submit" disabled={createAccount.isPending}>
          {createAccount.isPending ? 'Creating...' : 'Create Account'}
        </Button>
      </form>
    </Form>
  );
};
```

## 🎨 UI Components

### Design System

```typescript
// Button component with variants
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "underline-offset-4 hover:underline text-primary",
      },
      size: {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

### Chart Components

```typescript
// Analytics chart component
const AnalyticsChart = ({ data }: { data: AnalyticsData[] }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="transactions" 
          stroke="#8884d8" 
          strokeWidth={2}
        />
        <Line 
          type="monotone" 
          dataKey="volume" 
          stroke="#82ca9d" 
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

## 🔌 API Integration

### API Client

```typescript
// lib/api.ts
class APIClient {
  private baseURL: string;
  private apiKey: string;

  constructor(baseURL: string, apiKey: string) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Account methods
  accounts = {
    list: () => this.get<Account[]>('/api/v1/accounts/'),
    create: (data: AccountCreate) => this.post<Account>('/api/v1/accounts/', data),
    get: (id: string) => this.get<Account>(`/api/v1/accounts/${id}`),
  };

  // Transfer methods
  transfers = {
    list: () => this.get<Transfer[]>('/api/v1/transfers/'),
    create: (data: TransferCreate) => this.post<Transfer>('/api/v1/transfers/', data),
    get: (id: string) => this.get<Transfer>(`/api/v1/transfers/${id}`),
  };
}

export const api = new APIClient(
  import.meta.env.VITE_API_URL || 'http://localhost:8000',
  import.meta.env.VITE_API_KEY || ''
);
```

### Custom Hooks

```typescript
// hooks/use-api.ts
export const useAccounts = () => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: api.accounts.list,
    staleTime: 5 * 60 * 1000,
  });
};

export const useAccount = (id: string) => {
  return useQuery({
    queryKey: ['accounts', id],
    queryFn: () => api.accounts.get(id),
    enabled: !!id,
  });
};

export const useCreateAccount = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.accounts.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      toast.success('Account created successfully');
    },
    onError: (error) => {
      toast.error(`Failed to create account: ${error.message}`);
    },
  });
};
```

## 🎯 Performance Optimization

### Code Splitting

```typescript
// Lazy loading pages
const Dashboard = lazy(() => import('./pages/Dashboard'));
const AccountManagement = lazy(() => import('./pages/AccountManagement'));
const Transfers = lazy(() => import('./pages/Transfers'));

// App.tsx with Suspense
const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/accounts" element={<AccountManagement />} />
          <Route path="/transfers" element={<Transfers />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  </QueryClientProvider>
);
```

### Caching Strategy

```typescript
// Query client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});
```

## 🧪 Testing Strategy

### Component Testing

```typescript
// Component test example
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CreateAccountForm } from './CreateAccountForm';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

test('creates account successfully', async () => {
  const queryClient = createTestQueryClient();
  
  render(
    <QueryClientProvider client={queryClient}>
      <CreateAccountForm />
    </QueryClientProvider>
  );

  fireEvent.change(screen.getByLabelText(/network/i), {
    target: { value: 'stellar' }
  });
  
  fireEvent.change(screen.getByLabelText(/country/i), {
    target: { value: 'NG' }
  });
  
  fireEvent.click(screen.getByRole('button', { name: /create account/i }));
  
  await screen.findByText(/account created successfully/i);
});
```

## 🚀 Deployment

### Build Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          charts: ['recharts'],
        },
      },
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
```

### Environment Configuration

```typescript
// Environment variables
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_API_KEY: string;
  readonly VITE_APP_NAME: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TanStack Query Documentation](https://tanstack.com/query)
- [Radix UI Documentation](https://www.radix-ui.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Vite Documentation](https://vitejs.dev/)

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
