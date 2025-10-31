import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Support = () => {
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
          <Link className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/documentation">Docs</Link>
          <Link className="text-sm font-medium text-primary dark:text-primary transition-colors" to="/support">Support</Link>
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
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight tracking-tighter">We're Here to Help</h1>
            <p className="text-lg sm:text-xl text-gray-200 max-w-2xl">Get the support you need to build amazing payment applications with Rowell Infra.</p>
            <Link to="/register">
              <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                <span className="truncate">Get Started</span>
              </Button>
            </Link>
          </div>
        </section>

        {/* Support Options */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">How can we help you?</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Choose the support option that works best for you</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-16 w-16 rounded-full bg-primary/20 text-primary mx-auto mb-6">
                <span className="material-symbols-outlined text-2xl">help_outline</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Documentation</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Comprehensive guides, API references, and tutorials to help you get started.</p>
              <Link to="/documentation">
                <Button className="bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition-colors">
                  View Docs
                </Button>
              </Link>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-16 w-16 rounded-full bg-primary/20 text-primary mx-auto mb-6">
                <span className="material-symbols-outlined text-2xl">chat</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Community Support</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Join our developer community for peer-to-peer support and discussions.</p>
              <Button className="bg-primary/20 dark:bg-primary/20 text-primary dark:text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                Join Community
              </Button>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
              <div className="flex items-center justify-center h-16 w-16 rounded-full bg-primary/20 text-primary mx-auto mb-6">
                <span className="material-symbols-outlined text-2xl">email</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Email Support</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Get personalized help from our support team via email.</p>
              <Button className="bg-primary/20 dark:bg-primary/20 text-primary dark:text-white font-semibold py-2 px-4 rounded-lg hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                Contact Us
              </Button>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Frequently Asked Questions</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Find answers to common questions about our platform</p>
            </div>
            
            <div className="max-w-3xl mx-auto space-y-6">
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">How do I get started with Rowell Infra?</h3>
                <p className="text-gray-600 dark:text-gray-300">Getting started is easy! Simply sign up for a free account, get your API key, and start making API calls. Check out our <Link to="/documentation" className="text-primary hover:underline">documentation</Link> for detailed setup instructions.</p>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">What countries do you support?</h3>
                <p className="text-gray-600 dark:text-gray-300">We currently support over 20 African countries including Nigeria, Kenya, Ghana, South Africa, and many more. Our network is constantly expanding to include additional countries.</p>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">How fast are transfers?</h3>
                <p className="text-gray-600 dark:text-gray-300">Most transfers are completed within 3 seconds. Our platform uses advanced blockchain technology to ensure near-instantaneous settlements across our network.</p>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Is my data secure?</h3>
                <p className="text-gray-600 dark:text-gray-300">Yes, security is our top priority. We use bank-grade encryption, comply with international security standards, and undergo regular security audits to protect your data.</p>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Do you offer a sandbox environment?</h3>
                <p className="text-gray-600 dark:text-gray-300">Yes! All accounts include access to our sandbox environment where you can test your integration without processing real transactions.</p>
              </div>

              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">What programming languages do you support?</h3>
                <p className="text-gray-600 dark:text-gray-300">Our RESTful API works with any programming language. We also provide official SDKs for JavaScript, Python, PHP, and Java to make integration even easier.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Still need help?</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Get in touch with our support team</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">General Support</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">For general questions, technical issues, or account support.</p>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">email</span>
                  <span className="text-gray-600 dark:text-gray-300">support@rowellinfra.com</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">schedule</span>
                  <span className="text-gray-600 dark:text-gray-300">24/7 support</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">timer</span>
                  <span className="text-gray-600 dark:text-gray-300">Response time: &lt; 2 hours</span>
                </div>
              </div>
            </div>

            <div className="bg-background-light dark:bg-primary/10 p-8 rounded-xl border border-primary/20 dark:border-primary/20">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Enterprise Sales</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">For enterprise customers and custom solutions.</p>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">email</span>
                  <span className="text-gray-600 dark:text-gray-300">sales@rowellinfra.com</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">schedule</span>
                  <span className="text-gray-600 dark:text-gray-300">Business hours</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">timer</span>
                  <span className="text-gray-600 dark:text-gray-300">Response time: &lt; 4 hours</span>
                </div>
              </div>
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
              <Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" to="/documentation">Docs</Link>
              <Link className="text-sm text-primary dark:text-primary transition-colors" to="/support">Support</Link>
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

export default Support;
