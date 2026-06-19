"use client";

/**
 * AuthProvider — manages authentication state for the entire app.
 *
 * Token storage strategy:
 *   - Access token  → stored in a React ref (memory only — never persisted)
 *   - Refresh token → stored in localStorage (persists across page reloads)
 *
 * On mount, the provider attempts to restore the session by reading the
 * refresh token from localStorage and exchanging it for a fresh access token.
 */

import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";

import type { AuthContextType, User } from "@/types/auth";
import {
  exchangeCodeForTokens,
  getCurrentUser,
  getGitHubLoginUrl,
  refreshTokens,
} from "@/services/auth";

// ── Constants ──────────────────────────────────────────────────────────
const REFRESH_TOKEN_KEY = "gip_refresh_token";
const HAS_SESSION_KEY = "gip_has_session";

// ── Context ────────────────────────────────────────────────────────────
export const AuthContext = createContext<AuthContextType | null>(null);

// ── Provider ───────────────────────────────────────────────────────────
export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();

  // User state
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Access token lives in a ref — not in state — to avoid re-renders
  // every time it's refreshed in the background.
  const accessTokenRef = useRef<string | null>(null);

  /**
   * Redirect the user to GitHub's OAuth authorize page.
   */
  const login = useCallback(async () => {
    const url = await getGitHubLoginUrl();
    window.location.href = url;
  }, []);

  /**
   * Clear all auth state and redirect to the login page.
   */
  const logout = useCallback(() => {
    accessTokenRef.current = null;
    setUser(null);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(HAS_SESSION_KEY);
    document.cookie = "gip_has_session=; path=/; max-age=0"; // clear cookie
    router.push("/login");
  }, [router]);

  /**
   * Handle the OAuth callback: exchange the code for tokens,
   * fetch the user profile, and store everything.
   */
  const handleCallback = useCallback(
    async (code: string) => {
      try {
        const tokens = await exchangeCodeForTokens(code);

        // Store tokens
        accessTokenRef.current = tokens.access_token;
        localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
        localStorage.setItem(HAS_SESSION_KEY, "1");
        document.cookie = "gip_has_session=1; path=/; max-age=604800"; // 7 days

        // Fetch user profile
        const currentUser = await getCurrentUser(tokens.access_token);
        setUser(currentUser);

        // Navigate to dashboard
        router.push("/dashboard");
      } catch (error) {
        console.error("OAuth callback failed:", error);
        logout();
      }
    },
    [router, logout],
  );

  /**
   * Get the current access token. Returns null if not authenticated.
   */
  const getAccessToken = useCallback(() => {
    return accessTokenRef.current;
  }, []);

  /**
   * On mount: try to restore session from localStorage refresh token.
   */
  useEffect(() => {
    async function restoreSession() {
      const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

      if (!storedRefreshToken) {
        setIsLoading(false);
        return;
      }

      try {
        // Get fresh tokens
        const tokens = await refreshTokens(storedRefreshToken);
        accessTokenRef.current = tokens.access_token;
        localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);

        // Fetch user profile
        const currentUser = await getCurrentUser(tokens.access_token);
        setUser(currentUser);
      } catch (error) {
        // Refresh token is expired or invalid — clean up
        console.error("Session restore failed:", error);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem(HAS_SESSION_KEY);
        document.cookie = "gip_has_session=; path=/; max-age=0";
      } finally {
        setIsLoading(false);
      }
    }

    restoreSession();
  }, []);

  // ── Context value ──────────────────────────────────────────────────
  const value = useMemo<AuthContextType>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isLoading,
      login,
      logout,
      handleCallback,
      getAccessToken,
    }),
    [user, isLoading, login, logout, handleCallback, getAccessToken],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
