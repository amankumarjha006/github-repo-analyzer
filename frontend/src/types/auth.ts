/**
 * Authentication type definitions.
 *
 * Shared across services, hooks, and components.
 * Mirrors the backend Pydantic schemas.
 */

/** User profile as returned by GET /api/v1/users/me */
export interface User {
  id: string;
  github_id: number;
  username: string;
  email: string | null;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

/** Token pair returned by the backend after OAuth or refresh */
export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

/** Shape of the auth context exposed by AuthProvider */
export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: () => Promise<void>;
  logout: () => void;
  handleCallback: (code: string) => Promise<void>;
  getAccessToken: () => string | null;
}
