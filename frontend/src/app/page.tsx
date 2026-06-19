"use client";

/**
 * Home page — redirects to /login or /dashboard based on auth state.
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      router.push(isAuthenticated ? "/dashboard" : "/login");
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading spinner while determining auth state
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a]">
      <div className="h-12 w-12 animate-spin rounded-full border-4 border-white/10 border-t-purple-500" />
    </div>
  );
}