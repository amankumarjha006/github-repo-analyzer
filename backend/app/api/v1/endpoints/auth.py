"""Authentication endpoints — GitHub OAuth + token refresh.

Routes:
    GET  /github/login      → Returns the GitHub OAuth authorize URL.
    GET  /github/callback    → Exchanges code for tokens, upserts user.
    POST /refresh            → Exchanges a refresh token for new token pair.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.db.session import get_db
from app.schemas.token import TokenResponse
from app.services.auth import exchange_code_for_token, fetch_github_user
from app.services.user import get_or_create_user, get_user_by_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Step 1: Redirect the user to GitHub ───────────────────────────────────
@router.get("/github/login")
async def github_login():
    """Return the GitHub OAuth authorization URL.

    The frontend should redirect the browser to this URL.
    After the user authorizes, GitHub will redirect back to
    ``FRONTEND_URL/auth/callback?code=xxx``.
    """
    github_authorize_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.FRONTEND_URL}/auth/callback"
        f"&scope=user:email"
    )
    return {"url": github_authorize_url}


# ── Step 2: Handle the callback ───────────────────────────────────────────
@router.get("/github/callback", response_model=TokenResponse)
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Complete the OAuth flow after GitHub redirects back.

    1. Exchange the ``code`` for a GitHub access token.
    2. Use that token to fetch the GitHub user profile.
    3. Upsert the user in our database.
    4. Generate JWT access + refresh tokens.
    5. Return them to the frontend.

    Args:
        code: The authorization code from GitHub's redirect.
        db: Database session (injected).
    """
    # Exchange code → GitHub access token
    github_access_token = await exchange_code_for_token(code)

    # Fetch GitHub user profile
    github_user = await fetch_github_user(github_access_token)

    # Upsert user in our database
    user = await get_or_create_user(db, github_user)

    # Generate our own JWT tokens
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# ── Token Refresh ─────────────────────────────────────────────────────────
@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Issue a new access + refresh token pair from a valid refresh token.

    Args:
        refresh_token: The current (still-valid) refresh token.
        db: Database session (injected).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(refresh_token)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Make sure the user still exists
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    # Issue fresh tokens
    token_data = {"sub": str(user.id)}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )
