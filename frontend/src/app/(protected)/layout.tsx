"use client";

/**
 * Protected routes layout — guards all children under /(protected)/.
 *
 * If the user is not authenticated (and we're done loading), redirect
 * to /login. While loading, show a full-screen spinner.
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  // Still checking auth state
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a]">
        <div className="space-y-4 text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/10 border-t-purple-500" />
          <p className="text-sm text-gray-400">Loading your workspace...</p>
        </div>
      </div>
    );
  }

  // Not authenticated — will be redirected by the useEffect above
  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
