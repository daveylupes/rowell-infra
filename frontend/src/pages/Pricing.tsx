import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Pricing = () => {
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
          <Link className="text-sm font-medium text-primary dark:text-primary transition-colors" to="/pricing">Pricing</Link>
          <Link className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/documentation">Docs</Link>
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
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight tracking-tighter">Simple, Transparent Pricing</h1>
            <p className="text-lg sm:text-xl text-gray-200 max-w-2xl">Pay only for what you use. No hidden fees, no setup costs, no surprises.</p>
            <Link to="/register">
              <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                <span className="truncate">Get Started Free</span>
              </Button>
            </Link>
          </div>
        </section>

        {/* Pricing Cards */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Choose Your Plan</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Start free and scale as you grow. All plans include our core features.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Starter Plan */}
            <div className="bg-background-light dark:bg-background-dark p-8 rounded-xl border border-primary/20 dark:border-primary/20">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Starter</h3>
                <p className="text-gray-600 dark:text-gray-300 mt-2">Perfect for developers and small projects</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-gray-900 dark:text-white">$0</span>
                  <span className="text-gray-600 dark:text-gray-300">/month</span>
                </div>
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">1,000 API calls/month</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">5 countries supported</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Basic analytics</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Email support</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Sandbox environment</span>
                </li>
              </ul>
              <Link to="/register">
                <Button className="w-full bg-primary text-white font-semibold py-3 rounded-lg hover:bg-primary/90 transition-colors">
                  Get Started Free
                </Button>
              </Link>
            </div>

            {/* Professional Plan */}
            <div className="bg-background-light dark:bg-background-dark p-8 rounded-xl border-2 border-primary relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-primary text-white px-4 py-1 rounded-full text-sm font-semibold">Most Popular</span>
              </div>
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Professional</h3>
                <p className="text-gray-600 dark:text-gray-300 mt-2">For growing businesses and applications</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-gray-900 dark:text-white">$99</span>
                  <span className="text-gray-600 dark:text-gray-300">/month</span>
                </div>
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">50,000 API calls/month</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">15 countries supported</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Advanced analytics</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Priority support</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Webhook notifications</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Custom integrations</span>
                </li>
              </ul>
              <Link to="/register">
                <Button className="w-full bg-primary text-white font-semibold py-3 rounded-lg hover:bg-primary/90 transition-colors">
                  Start Professional
                </Button>
              </Link>
            </div>

            {/* Enterprise Plan */}
            <div className="bg-background-light dark:bg-background-dark p-8 rounded-xl border border-primary/20 dark:border-primary/20">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Enterprise</h3>
                <p className="text-gray-600 dark:text-gray-300 mt-2">For large-scale operations</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-gray-900 dark:text-white">Custom</span>
                </div>
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Unlimited API calls</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">All 20+ countries</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">Custom analytics</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">24/7 dedicated support</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">SLA guarantees</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary text-sm">check</span>
                  <span className="text-gray-600 dark:text-gray-300">On-premise deployment</span>
                </li>
              </ul>
              <Link to="/support">
                <Button className="w-full bg-primary/20 dark:bg-primary/20 text-primary dark:text-white font-semibold py-3 rounded-lg hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                  Contact Sales
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Additional Pricing Info */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Additional Pricing</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Transparent pricing for all services</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Transfer Fees</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Domestic transfers</span>
                    <span className="font-semibold text-gray-900 dark:text-white">0.25%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Cross-border transfers</span>
                    <span className="font-semibold text-gray-900 dark:text-white">0.5%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Minimum fee</span>
                    <span className="font-semibold text-gray-900 dark:text-white">$0.50</span>
                  </div>
                </div>
              </div>
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Account Management</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Account creation</span>
                    <span className="font-semibold text-gray-900 dark:text-white">Free</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Monthly maintenance</span>
                    <span className="font-semibold text-gray-900 dark:text-white">$0.10/account</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Account verification</span>
                    <span className="font-semibold text-gray-900 dark:text-white">$1.00/account</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Frequently Asked Questions</h2>
          </div>
          <div className="max-w-3xl mx-auto space-y-8">
            <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Can I change plans anytime?</h3>
              <p className="text-gray-600 dark:text-gray-300">Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.</p>
            </div>
            <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">What happens if I exceed my API limits?</h3>
              <p className="text-gray-600 dark:text-gray-300">We'll notify you when you're approaching your limits. Additional usage is charged at $0.01 per API call.</p>
            </div>
            <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Do you offer custom pricing?</h3>
              <p className="text-gray-600 dark:text-gray-300">Yes, we offer custom pricing for enterprise customers with high-volume needs. Contact our sales team for details.</p>
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
              <Link className="text-sm text-primary dark:text-primary transition-colors" to="/pricing">Pricing</Link>
              <Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/documentation">Docs</Link>
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

export default Pricing;
