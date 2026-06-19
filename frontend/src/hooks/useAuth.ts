"use client";

/**
 * useAuth — convenience hook to access the auth context.
 *
 * Throws a descriptive error if used outside of AuthProvider,
 * so you get an immediate stack trace instead of a silent null.
 */

import { useContext } from "react";

import { AuthContext } from "@/providers/AuthProvider";
import type { AuthContextType } from "@/types/auth";

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error(
      "useAuth() must be used within an <AuthProvider>. " +
        "Wrap your component tree with <AuthProvider> in layout.tsx.",
    );
  }

  return context;
}
