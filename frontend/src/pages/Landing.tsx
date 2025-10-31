import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import Header from "@/components/Header";

const Landing = () => {
  return (
    <div className="relative flex flex-col min-h-screen w-full">
      <Header />

      <main className="flex flex-col">
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center text-center px-4 sm:px-6 lg:px-8 py-20">
          <div className="absolute inset-0 bg-cover bg-center" style={{backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.8) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuCkQVbCfQvwHWDAIllCKYBnYqWyxPbWPzYFioTOwQEH_CJpc0km4xwTV15HJLlOTly-cNrBA3qcBBq__jCvClQSP6tiHyC8A90JtmAyL8Fu8PGw4BQNlnbboxlVSwweSCjHf7ocZhPGQj1cPvC_zuok9GvXe_lpwfQ6f2l7fVVhHkUAOH0995oniLJuSADxb6wpPgAAvZ6Q_VRUVAEb-g8uRPEBNGQMceVQBehtXGbZS-vZkQp-YXS5rkYoGRoo1xOCYerSCdiT3BNe")'}}></div>
          <div className="relative z-10 max-w-4xl mx-auto flex flex-col items-center gap-6">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight tracking-tighter">Build the future of African payments</h1>
            <p className="text-lg sm:text-xl text-gray-200 max-w-2xl">Rowell Infra is the infrastructure platform that makes building cross-border payment applications for Africa as simple as sending an email.</p>
            <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
              <span className="truncate">Start Building</span>
            </Button>
          </div>
        </section>

        {/* Problem Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">The Problem</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Traditional remittance systems are slow, expensive, and fragmented, hindering economic growth and financial inclusion across Africa.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex flex-col gap-4 items-center text-center bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                <span className="material-symbols-outlined">payments</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">High Fees</h3>
              <p className="text-gray-600 dark:text-gray-300">Average remittance fees to Africa are among the highest globally, eroding the value of hard-earned money.</p>
            </div>
            <div className="flex flex-col gap-4 items-center text-center bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                <span className="material-symbols-outlined">hourglass_empty</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Slow Settlements</h3>
              <p className="text-gray-600 dark:text-gray-300">Settlement times can take days, delaying critical financial support for families and businesses.</p>
            </div>
            <div className="flex flex-col gap-4 items-center text-center bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                <span className="material-symbols-outlined">public_off</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Limited Reach</h3>
              <p className="text-gray-600 dark:text-gray-300">Many African countries lack seamless cross-border payment infrastructure, limiting economic opportunities.</p>
            </div>
          </div>
        </section>

        {/* Solution Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Our Solution</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Rowell Infra provides a unified, fast, and cost-effective platform for building cross-border payment applications across Africa.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="flex flex-col gap-4 items-center text-center p-6">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                  <span className="material-symbols-outlined">api</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Unified API</h3>
                <p className="text-gray-600 dark:text-gray-300">A single, intuitive API simplifies integration and reduces development time.</p>
              </div>
              <div className="flex flex-col gap-4 items-center text-center p-6">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                  <span className="material-symbols-outlined">bolt</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">3-Second Settlements</h3>
                <p className="text-gray-600 dark:text-gray-300">Experience near-instantaneous settlements, enabling real-time transactions.</p>
              </div>
              <div className="flex flex-col gap-4 items-center text-center p-6">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary">
                  <span className="material-symbols-outlined">public</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">20+ African Countries</h3>
                <p className="text-gray-600 dark:text-gray-300">Access a growing network of over 20 African countries, with more added regularly.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-center">
            <div className="bg-primary/10 dark:bg-primary/20 p-8 rounded-xl">
              <p className="text-base font-medium text-primary dark:text-gray-200">African Remittance Market</p>
              <p className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mt-2">$86B+</p>
            </div>
            <div className="bg-primary/10 dark:bg-primary/20 p-8 rounded-xl">
              <p className="text-base font-medium text-primary dark:text-gray-200">Mobile Money Users in Africa</p>
              <p className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mt-2">500M+</p>
            </div>
          </div>
        </section>

        {/* Trusted By Section */}
        <section className="py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight text-center mb-12">Trusted by innovative companies</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-8 items-center">
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCzJJVmElNEegNnQtbDpA234peIzRz6mUXxdvI8qsQKk87kMV9UhVmdy0ms3ELESgOhoZc7Cmsy10Yx422kVSMj-muUabLIb_mMZXsYG2MXgl3uwb33y734hoqz4UrxQ6mtgneYyGGfbeplSza0Zel5A5csH9W-QleAX3O1TQYSSTdXu8k79C1CN_VETJwv_VvE_zvjahTRONfDko3_9fiXV3prF6GEwp0cfZOp4E-h-aTFzErMIkt02W_MnFJC8YrHr6iZz0JktC-h")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDZG5p0aO5coGl_CNJ4cRWsGMfNDaEXs8Lqb5g2Ogy9V0xAlUBkqWe-8N-VBvvJPy-LnL_7jmMj2b_RL90QPFshvFNSG6Z3qS4AqnAzTdTKkEnHLk2RznJOuZwzyIAtjh-u3HfTV4jtrYi137VptWBiFSCFtn3OEZ7R47GSnx06KfXbLcdp3op9YUu3syAfJJDS6RRFKtpIQQnmEYUFsAvpdBYxRQvAL39TlZ7h4ByE34O6Xc2qvxh45OeOR-3XNzzxjr5ht86pN7Iq")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAip9qnjKOxYVsaaiQGKtamnBBQ-jjg6FYyqx4f0hnHhRAS4LibK-y4VmdGD2Ww8y_sKIbsSgv7TI9uFVcNy3sy6PJY8WFbB2VyyQsfGY4ov0cFOZpg4a8m7xtcP2xwwEMA7_HMJ1-leFlkEtzSNskaZzLTFyLGmP4Amn5ZI6FC4-XPXKc2Ib3BH9HPtFVLG1iUP-7cwHjYSkmus_iuMmwBZxHTS8X8HWmgLe2v-TE66k7BVa5dpXuME2SnMrBq1x1GI78rz9kuSjoa")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCSFJU1ZKlkfocleYm8YqioCV3IzeFilTl-SoKm1oTSE6Z7cW1IXevIigpPNBNxZSHzy3I2xauDJGIk7vVFjypllcTqvGPOWU1YmkCwwdko4BtXZkczupU0ofP821RSabqJuEUltLlG17PFGKc5aJJe-GNIXlhjP-_XgAkgC6QSr1Ph5Nnx02WoM1vyguEDszshoMI4dGD3WV-4B-Od4M_F1D3UxBY2fSjdlubmSUlP_hDwOqJdKzsoNI3fn6Ee8gLYOMzIPrjgQIlK")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAlwxPJNd6b6lv_8_dZ--6i6gk2hN-vJ9foqtV_iI5aFpLKs08ytAvrxbpyYxu5CAmfw0luid615c_y1qkZZEPv4fW3Y0cIr_pczCiXxqsfmV2QEQHwQaj0vpdnA1kTHjVzueNh63_mD4esa2xPm-kdbF7WwVJ9k0qiNxL8Oq7Y57d1oyibw-j7tIbucLjrMqXlNa5R-dYQzOPtheWiTIbmBLPvAo3DsW8mQ432dI1wV25UV03_oJhIK34dzG7N2GDNoIPA4ZVxJNs1")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
              <div className="w-full h-24 bg-center bg-no-repeat bg-contain rounded-lg" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBywXJvOwDi41E7ADNv8tCH3a6FEZmFZF7MknnMEH1gDh7FVUzBuf-5bpd0w1NE9VRDVLKozGp35toLkfO82oyaPQi9--2H7v5ktoUKlZcgMW9agAod-Vi4dFqU7hgZ7r7OD_FawlttlVqz93Kf884KPlHHQVOF-6aA5YvxkDbMKZcipQox5Ec-RlHDpf-qY6YZvonZAw8Z--nxJquH0kyi7eBBS_DPnckdFZo3phWLLBDfd6TONUa86uCE9eoBUMLRAQPIfiiTOBfy")', filter: 'grayscale(1) brightness(2) contrast(0.5)'}}></div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-primary/5 dark:bg-primary/10 py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white tracking-tight">Ready to build the future of African payments?</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">Join the growing community of developers and businesses leveraging Rowell Infra's powerful platform.</p>
              <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
                <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/90 transition-colors">
                  <span className="truncate">Start Building</span>
                </Button>
                <Button className="flex items-center justify-center rounded-lg h-12 px-6 bg-primary/20 dark:bg-primary/20 text-primary dark:text-white text-base font-bold leading-normal tracking-wide hover:bg-primary/30 dark:hover:bg-primary/30 transition-colors">
                  <span className="truncate">View Documentation</span>
                </Button>
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

export default Landing;