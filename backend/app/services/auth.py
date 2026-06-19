"""GitHub OAuth service.

Handles the two-step OAuth exchange:
  1. Exchange the temporary ``code`` for a GitHub access token.
  2. Use that token to fetch the authenticated GitHub user profile.
"""

import httpx
from fastapi import HTTPException, status

from app.core.config import settings

# GitHub OAuth endpoints
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


async def exchange_code_for_token(code: str) -> str:
    """Exchange an OAuth authorization code for a GitHub access token.

    Args:
        code: The ``code`` query-param GitHub sends to our callback URL.

    Returns:
        The GitHub access token string.

    Raises:
        HTTPException: If the exchange fails (bad code, expired, etc.).
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )

    data = response.json()

    if "access_token" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub OAuth failed: {data.get('error_description', 'unknown error')}",
        )

    return data["access_token"]


async def fetch_github_user(access_token: str) -> dict:
    """Fetch the authenticated GitHub user's profile.

    Args:
        access_token: A valid GitHub access token.

    Returns:
        Dict containing GitHub user data (id, login, email, avatar_url, etc.).

    Raises:
        HTTPException: If the GitHub API request fails.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch GitHub user profile.",
        )

    return response.json()
