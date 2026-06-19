"use client";

/**
 * OAuth callback page — /auth/callback
 *
 * GitHub redirects here with ?code=xxx after the user authorizes.
 * This page extracts the code, sends it to the backend, and lets
 * the AuthProvider handle token storage + redirect to /dashboard.
 */

import { useEffect, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { useAuth } from "@/hooks/useAuth";

function CallbackHandler() {
  const searchParams = useSearchParams();
  const { handleCallback } = useAuth();
  const hasRun = useRef(false);

  useEffect(() => {
    // Prevent double-execution in React Strict Mode
    if (hasRun.current) return;

    const code = searchParams.get("code");

    if (code) {
      hasRun.current = true;
      handleCallback(code);
    } else {
      // No code param — something went wrong
      window.location.href = "/login";
    }
  }, [searchParams, handleCallback]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a]">
      <div className="text-center space-y-4">
        {/* Spinner */}
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/10 border-t-purple-500" />
        <p className="text-lg font-medium text-white">
          Authenticating with GitHub...
        </p>
        <p className="text-sm text-gray-500">
          Please wait while we complete your sign-in.
        </p>
      </div>
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a]">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-white/10 border-t-purple-500" />
        </div>
      }
    >
      <CallbackHandler />
    </Suspense>
  );
}
