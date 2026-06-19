/**
 * Auth service — API calls to the backend auth endpoints.
 *
 * All fetch calls go through these functions so that the rest of the
 * frontend never constructs URLs or handles raw responses directly.
 */

import type { AuthTokens, User } from "@/types/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Step 1: Get the GitHub OAuth authorization URL from the backend.
 * The frontend should redirect `window.location.href` to this URL.
 */
export async function getGitHubLoginUrl(): Promise<string> {
  const response = await fetch(`${API_URL}/api/v1/auth/github/login`);
  const data = await response.json();
  return data.url;
}

/**
 * Step 2: Exchange the GitHub `code` for our JWT token pair.
 * Called from the /auth/callback page after GitHub redirects back.
 */
export async function exchangeCodeForTokens(
  code: string,
): Promise<AuthTokens> {
  const response = await fetch(
    `${API_URL}/api/v1/auth/github/callback?code=${code}`,
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Authentication failed");
  }

  return response.json();
}

/**
 * Refresh the access token using a valid refresh token.
 */
export async function refreshTokens(
  refreshToken: string,
): Promise<AuthTokens> {
  const response = await fetch(
    `${API_URL}/api/v1/auth/refresh?refresh_token=${encodeURIComponent(refreshToken)}`,
    { method: "POST" },
  );

  if (!response.ok) {
    throw new Error("Token refresh failed");
  }

  return response.json();
}

/**
 * Fetch the current user's profile using an access token.
 */
export async function getCurrentUser(accessToken: string): Promise<User> {
  const response = await fetch(`${API_URL}/api/v1/users/me`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return response.json();
}
