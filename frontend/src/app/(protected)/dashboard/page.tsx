"use client";

/**
 * Dashboard page — the main landing page after login.
 *
 * Shows the user's profile and provides a logout button.
 */

import { useAuth } from "@/hooks/useAuth";

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-[#0a0a0a] p-8">
      {/* Header */}
      <header className="mx-auto flex max-w-6xl items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-blue-600 text-sm font-bold text-white shadow-lg shadow-purple-500/25">
            GI
          </div>
          <h1 className="text-xl font-bold text-white">
            GitHub Intelligence
          </h1>
        </div>

        <div className="flex items-center gap-4">
          {user?.avatar_url && (
            <img
              src={user.avatar_url}
              alt={user.username}
              className="h-8 w-8 rounded-full ring-2 ring-white/10"
            />
          )}
          <span className="text-sm text-gray-300">{user?.username}</span>
          <button
            id="logout-btn"
            onClick={logout}
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-300 transition-colors hover:bg-white/10 hover:text-white"
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto mt-12 max-w-6xl">
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-8">
          <h2 className="text-2xl font-bold text-white">
            Welcome back, {user?.username} 👋
          </h2>
          <p className="mt-2 text-gray-400">
            Your GitHub Intelligence dashboard is ready. Start analyzing
            repositories to get insights.
          </p>

          {/* Quick Stats Grid (placeholder) */}
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6">
              <p className="text-sm text-gray-500">Repositories Analyzed</p>
              <p className="mt-1 text-3xl font-bold text-white">0</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6">
              <p className="text-sm text-gray-500">Average Health Score</p>
              <p className="mt-1 text-3xl font-bold text-white">—</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6">
              <p className="text-sm text-gray-500">Total Insights</p>
              <p className="mt-1 text-3xl font-bold text-white">0</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
