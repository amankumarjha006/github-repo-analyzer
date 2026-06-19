"use client";

/**
 * Analysis page — placeholder for deep analysis feature.
 */

import { useAuth } from "@/hooks/useAuth";

export default function AnalysisPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-[#0a0a0a] p-8">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-2xl font-bold text-white">Analysis</h1>
        <p className="mt-2 text-gray-400">
          Deep repository analysis will be implemented here, {user?.username}.
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
                d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"
              />
            </svg>
          </div>
          <p className="text-lg font-medium text-gray-300">
            No analyses available
          </p>
          <p className="mt-1 text-sm text-gray-500">
            This feature will be available after auth is complete.
          </p>
        </div>
      </div>
    </div>
  );
}
