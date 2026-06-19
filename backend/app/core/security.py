"""JWT token creation and verification.

All token logic is centralised here so that the rest of the app never
touches ``python-jose`` directly.

Tokens use HS256 (symmetric) — adequate for a single-service backend.
For a multi-service architecture, consider RS256 (asymmetric).
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


# ── Access Token ──────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a short-lived JWT for authenticating API requests.

    Args:
        data: Payload dict — must include ``"sub"`` (user id as string).
        expires_delta: Custom expiry.  Defaults to ``ACCESS_TOKEN_EXPIRE_MINUTES``.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# ── Refresh Token ─────────────────────────────────────────────────────────
def create_refresh_token(data: dict) -> str:
    """Create a long-lived JWT used to obtain new access tokens.

    Args:
        data: Payload dict — must include ``"sub"`` (user id as string).

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# ── Verification ──────────────────────────────────────────────────────────
def verify_token(token: str) -> dict:
    """Decode and verify a JWT.

    Args:
        token: The raw JWT string.

    Returns:
        The decoded payload dict.

    Raises:
        JWTError: If the token is invalid, expired, or tampered with.
    """
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
