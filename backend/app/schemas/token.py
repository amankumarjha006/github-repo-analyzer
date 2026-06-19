"""Pydantic schemas for JWT token payloads and responses."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Returned to the client after successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Decoded JWT payload — used internally for verification."""

    sub: str  # user UUID as string
    type: str  # "access" or "refresh"
    exp: int  # expiry timestamp
