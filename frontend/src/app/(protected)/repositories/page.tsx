"use client";

/**
 * Repositories page — placeholder for the repo analysis feature.
 */

import { useAuth } from "@/hooks/useAuth";

export default function RepositoriesPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-[#0a0a0a] p-8">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-2xl font-bold text-white">Repositories</h1>
        <p className="mt-2 text-gray-400">
          Repository analysis will be implemented here, {user?.username}.
        </p>

        <div className="mt-8 rounded-2xl border border-dashed border-white/10 bg-white/[0.02] p-12 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5 text-gray-500">
            <svg
              className="h-8 w-8"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776"
              />
            </svg>
          </div>
          <p className="text-lg font-medium text-gray-300">
            No repositories analyzed yet
          </p>
          <p className="mt-1 text-sm text-gray-500">
            This feature will be available after auth is complete.
          </p>
        </div>
      </div>
    </div>
  );
}
