import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { useEffect } from "react";

const Documentation = () => {
  const navigate = useNavigate();

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  // Function to handle navigation with scroll to top
  const handleNavigation = (path: string) => {
    navigate(path);
    window.scrollTo(0, 0);
  };

  const quickStartSteps = [
    {
      step: 1,
      title: "Get Your API Key",
      description: "Sign up for a free account and get your API key",
      action: "Sign Up"
    },
    {
      step: 2,
      title: "Install SDK",
      description: "Choose your preferred SDK and install it",
      action: "View SDKs"
    },
    {
      step: 3,
      title: "Make Your First Call",
      description: "Create an account and send your first transfer",
      action: "Try API"
    }
  ];

  const apiExamples = [
    {
      title: "Create Account",
      language: "JavaScript",
      code: `const account = await rowell.accounts.create({
  network: 'stellar',
  country_code: 'NG',
  account_type: 'user'
});`
    },
    {
      title: "Send Transfer",
      language: "Python",
      code: `transfer = await rowell.transfers.create({
  from_account: 'account_id',
  to_account: 'recipient_id',
  amount: '100.00',
  currency: 'USD'
});`
    },
    {
      title: "Get Balance",
      language: "cURL",
      code: `curl -X GET \\
  https://api.rowellinfra.com/v1/accounts/balance \\
  -H "Authorization: Bearer YOUR_API_KEY"`
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 flex items-center justify-between whitespace-nowrap border-b border-primary/20 dark:border-primary/10 bg-background-light/80 dark:bg-background-dark/80 px-4 sm:px-6 lg:px-10 py-3 backdrop-blur-sm">
        <Link to="/" className="flex items-center gap-4">
          <svg className="h-8 w-8 text-primary" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path clipRule="evenodd" d="M39.475 21.6262C40.358 21.4363 40.6863 21.5589 40.7581 21.5934C40.7876 21.655 40.8547 21.857 40.8082 22.3336C40.7408 23.0255 40.4502 24.0046 39.8572 25.2301C38.6799 27.6631 36.5085 30.6631 33.5858 33.5858C30.6631 36.5085 27.6632 38.6799 25.2301 39.8572C24.0046 40.4502 23.0255 40.7407 22.3336 40.8082C21.8571 40.8547 21.6551 40.7875 21.5934 40.7581C21.5589 40.6863 21.4363 40.358 21.6262 39.475C21.8562 38.4054 22.4689 36.9657 23.5038 35.2817C24.7575 33.2417 26.5497 30.9744 28.7621 28.762C30.9744 26.5497 33.2417 24.7574 35.2817 23.5037C36.9657 22.4689 38.4054 21.8562 39.475 21.6262ZM4.41189 29.2403L18.7597 43.5881C19.8813 44.7097 21.4027 44.9179 22.7217 44.7893C24.0585 44.659 25.5148 44.1631 26.9723 43.4579C29.9052 42.0387 33.2618 39.5667 36.4142 36.4142C39.5667 33.2618 42.0387 29.9052 43.4579 26.9723C44.1631 25.5148 44.659 24.0585 44.7893 22.7217C44.9179 21.4027 44.7097 19.8813 43.5881 18.7597L29.2403 4.41187C27.8527 3.02428 25.8765 3.02573 24.2861 3.36776C22.6081 3.72863 20.7334 4.58419 18.8396 5.74801C16.4978 7.18716 13.9881 9.18353 11.5858 11.5858C9.18354 13.988 7.18717 16.4978 5.74802 18.8396C4.58421 20.7334 3.72865 22.6081 3.36778 24.2861C3.02574 25.8765 3.02429 27.8527 4.41189 29.2403Z" fill="currentColor" fillRule="evenodd"></path>
          </svg>
          <h2 className="text-xl font-bold leading-tight text-gray-900 dark:text-white tracking-tight">Rowell Infra</h2>
        </Link>
        <nav className="hidden md:flex items-center gap-8">
          <Link className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/product">Product</Link>
          <Link className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/pricing">Pricing</Link>
          <Link className="text-sm font-medium text-primary dark:text-primary transition-colors" to="/documentation">Docs</Link>
          <Link className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/support">Support</Link>
        </nav>
        <div className="hidden md:flex items-center gap-2">
          <Link to="/register">
            <Button className="flex items-center justify-center rounded h-9 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
              <span className="truncate">Start Building</span>
            </Button>
          </Link>
          <Link to="/login">
            <Button className="flex items-center justify-center rounded h-9 px-4 bg-primary/20 dark:bg-primary/20 text-primary dark:text-white text-sm font-bold leading-normal tracking-wide hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
              <span className="truncate">Sign In</span>
            </Button>
          </Link>
        </div>
      </header>

      <main className="flex flex-col">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center text-center px-4 sm:px-6 lg:px-8 py-20">
          <div className="absolute inset-0 bg-cover bg-center" style={{backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.8) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuCkQVbCfQvwHWDAIllCKYBnYqWyxPbWPzYFioTOwQEH_CJpc0km4xwTV15HJLlOTly-cNrBA3qcBBq__jCvClQSP6tiHyC8A90JtmAyL8Fu8PGw4BQNlnbboxlVSwweSCjHf7ocZhPGQj1cPvC_zuok9GvXe_lpwfQ6f2l7fVVhHkUAOH0995oniLJuSADxb6wpPgAAvZ6Q_VRUVAEb-g8uRPEBNGQMceVQBehtXGbZS-vZkQp-YXS5rkYoGRoo1xOCYerSCdiT3BNe")'}}></div>
          <div className="relative z-10 max-w-4xl mx-auto flex flex-col items-center gap-6">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight tracking-tighter">Developer Documentation</h1>
            <p className="text-lg sm:text-xl text-gray-200 max-w-2xl">Everything you need to build powerful payment applications across Africa</p>
            <Link to="/register">
              <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                <span className="truncate">Get Started</span>
              </Button>
            </Link>
          </div>
        </section>

        {/* Quick Start Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Get Started in 3 Steps</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">From signup to your first API call in minutes</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {quickStartSteps.map((step, index) => (
              <div key={index} className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl font-bold text-primary">{step.step}</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">{step.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">{step.description}</p>
                <Button 
                  className="bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition-colors"
                  onClick={() => {
                    if (step.step === 1) {
                      handleNavigation('/register');
                    } else if (step.step === 2) {
                      // Scroll to SDKs section
                      document.getElementById('sdks-section')?.scrollIntoView({ behavior: 'smooth' });
                    } else if (step.step === 3) {
                      // Scroll to API examples section
                      document.getElementById('api-examples-section')?.scrollIntoView({ behavior: 'smooth' });
                    }
                  }}
                >
                  {step.action}
                </Button>
              </div>
            ))}
          </div>
        </section>

        {/* API Examples Section */}
        <section id="api-examples-section" className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">API Examples</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">See how easy it is to integrate with our API</p>
            </div>
            
            <div className="space-y-8">
              {apiExamples.map((example, index) => (
                <div key={index} className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{example.title}</h3>
                    <span className="px-3 py-1 bg-primary/20 text-primary text-sm font-medium rounded-full">{example.language}</span>
                  </div>
                  <div className="bg-gray-900 dark:bg-gray-800 rounded-lg p-4 text-sm font-mono text-green-400 overflow-x-auto">
                    <pre>{example.code}</pre>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* SDKs Section */}
        <section id="sdks-section" className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Official SDKs</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Choose your preferred programming language</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-16 h-16 bg-yellow-500 rounded-lg flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">JS</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">JavaScript/TypeScript</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Full-featured SDK with TypeScript support for web and Node.js</p>
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg font-mono text-sm mb-6">
                npm install @rowell/infra-sdk
              </div>
              <Button 
                className="w-full bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition-colors"
                onClick={() => {
                  // For now, just scroll to top since we don't have individual SDK docs
                  window.scrollTo(0, 0);
                }}
              >
                View Documentation
              </Button>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-lg flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">PY</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Python</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Async Python SDK with full API coverage and Django support</p>
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg font-mono text-sm mb-6">
                pip install rowell-infra
              </div>
              <Button 
                className="w-full bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition-colors"
                onClick={() => {
                  // For now, just scroll to top since we don't have individual SDK docs
                  window.scrollTo(0, 0);
                }}
              >
                View Documentation
              </Button>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="w-16 h-16 bg-cyan-500 rounded-lg flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">FL</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Flutter</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Cross-platform mobile SDK for iOS, Android, and web</p>
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg font-mono text-sm mb-6">
                flutter pub add rowell_infra
              </div>
              <Button 
                className="w-full bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition-colors"
                onClick={() => {
                  // For now, just scroll to top since we don't have individual SDK docs
                  window.scrollTo(0, 0);
                }}
              >
                View Documentation
              </Button>
            </div>
          </div>
        </section>

        {/* Resources Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Additional Resources</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Everything you need to build with Rowell Infra</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="material-symbols-outlined text-primary">api</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">API Reference</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Complete API endpoint documentation</p>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  onClick={() => handleNavigation('/api-reference')}
                >
                  View Reference
                </Button>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="material-symbols-outlined text-primary">rocket_launch</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Quickstart Guide</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Get up and running in 5 minutes</p>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  onClick={() => handleNavigation('/quickstart')}
                >
                  Start Guide
                </Button>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="material-symbols-outlined text-primary">code</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Code Examples</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Real-world implementation examples</p>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  onClick={() => {
                    // For now, just scroll to top since we don't have a code examples page
                    window.scrollTo(0, 0);
                  }}
                >
                  View Examples
                </Button>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="material-symbols-outlined text-primary">help_outline</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Support</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">Get help from our team</p>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  onClick={() => handleNavigation('/support')}
                >
                  Get Support
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Ready to start building?</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">Join thousands of developers building the future of African payments.</p>
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
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-background-light dark:bg-background-dark border-t border-primary/20 dark:border-primary/10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <nav className="flex flex-wrap justify-center gap-x-6 gap-y-2">
              <Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/product">Product</Link>
              <Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/pricing">Pricing</Link>
              <Link className="text-sm text-primary dark:text-primary transition-colors" to="/documentation">Docs</Link>
              <Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/support">Support</Link>
              <a className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="#">Terms of Service</a>
              <a className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="#">Privacy Policy</a>
            </nav>
            <p className="text-sm text-gray-500 dark:text-gray-400">© 2025 Rowell Infra. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Documentation;
