import { Link, useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { ReactNode } from "react";

interface DashboardLayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

export function DashboardLayout({ children, title, description }: DashboardLayoutProps) {
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigationItems = [
    { path: "/dashboard", icon: "dashboard", label: "Dashboard" },
    { path: "/developer-dashboard", icon: "key", label: "API Keys" },
    { path: "/accounts", icon: "group", label: "Accounts" },
    { path: "/transfers", icon: "swap_horiz", label: "Transfers" },
    { path: "/analytics", icon: "bar_chart", label: "Analytics" },
  ];

  const isActive = (path: string) => {
    if (path === "/dashboard") {
      return location.pathname === "/dashboard";
    }
    return location.pathname.startsWith(path);
  };

  const displayName = user ? `${user.first_name} ${user.last_name}` : "User";

  return (
    <div className="relative flex min-h-screen w-full font-display bg-background-light dark:bg-background-dark text-deep-teal dark:text-gray-200">
      {/* SideNavBar */}
      <aside className="flex h-screen w-64 flex-col justify-between bg-deep-teal p-4 text-white sticky top-0">
        <div className="flex flex-col gap-8">
          <div className="flex items-center gap-3 px-3">
            <span className="material-symbols-outlined text-3xl from-accent-start to-accent-end bg-gradient-to-tr text-transparent bg-clip-text">
              data_object
            </span>
            <h1 className="text-white text-xl font-bold leading-normal">Rowell Infra</h1>
          </div>
          <nav className="flex flex-col gap-2">
            {navigationItems.map((item) => {
              const active = isActive(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                    active
                      ? "bg-gradient-to-r from-accent-start to-accent-end text-white shadow-lg"
                      : "hover:bg-white/10"
                  }`}
                >
                  <span
                    className={`material-symbols-outlined ${
                      active ? "text-white" : "text-white/80"
                    }`}
                  >
                    {item.icon}
                  </span>
                  <p
                    className={`text-sm leading-normal ${
                      active ? "font-bold" : "font-medium"
                    }`}
                  >
                    {item.label}
                  </p>
                </Link>
              );
            })}
          </nav>
        </div>
        <div className="flex flex-col gap-4">
          <Link
            to="/api-reference"
            className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <span className="material-symbols-outlined text-white/80">menu_book</span>
            <p className="text-sm font-medium leading-normal">API Documentation</p>
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex flex-1 flex-col">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 px-8 py-4 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Welcome,</p>
            <p className="text-sm font-bold text-deep-teal dark:text-white">{displayName}</p>
          </div>
          <button
            onClick={logout}
            className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-deep-teal dark:text-white text-sm font-bold leading-normal tracking-[0.015em] gap-2 transition-colors"
          >
            <span className="material-symbols-outlined text-base">logout</span>
            <span className="truncate">Logout</span>
          </button>
        </header>

        <div className="flex-1 p-8">
          <div className="mx-auto max-w-7xl">
            {/* Page Heading - only show if title is provided */}
            {(title || description) && (
              <div className="mb-8">
                {title && (
                  <h1 className="text-deep-teal dark:text-white text-3xl font-bold leading-tight tracking-tight">
                    {title}
                  </h1>
                )}
                {description && (
                  <p className="text-gray-500 dark:text-gray-400 text-base font-normal leading-normal mt-1">
                    {description}
                  </p>
                )}
              </div>
            )}

            {/* Page Content */}
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
