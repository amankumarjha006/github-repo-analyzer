/**
 * Next.js Edge Middleware — route protection.
 *
 * Runs on every matched request BEFORE the page renders.
 *
 * Strategy:
 *   - We can't access localStorage from Edge middleware, so we check
 *     for a `gip_has_session` cookie as a **hint** that the user has
 *     logged in before.
 *   - The real auth guard lives in the (protected)/layout.tsx on the
 *     client side. This middleware is a fast first-pass to avoid
 *     flashing protected content before the client hydrates.
 *
 * Routes:
 *   /dashboard, /repositories, /analysis → require session hint
 *   /login → redirect to /dashboard if session hint exists
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Paths that require authentication
const protectedPaths = ["/dashboard", "/repositories", "/analysis"];

// Paths that should redirect away if already authenticated
const authPaths = ["/login"];

export default function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = request.cookies.get("gip_has_session")?.value === "1";

  // Protected routes: redirect to /login if no session hint
  if (protectedPaths.some((path) => pathname.startsWith(path))) {
    if (!hasSession) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  // Auth routes: redirect to /dashboard if session exists
  if (authPaths.some((path) => pathname.startsWith(path))) {
    if (hasSession) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/repositories/:path*", "/analysis/:path*", "/login"],
};
