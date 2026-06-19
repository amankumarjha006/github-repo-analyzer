"""FastAPI dependency functions for authentication.

These are injected via ``Depends(...)`` into route handlers that
require a logged-in user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.db.session import get_db
from app.services.user import get_user_by_id

# The tokenUrl doesn't need to point at a real endpoint — it's only used
# by the Swagger UI "Authorize" button.  Our real auth flow is GitHub OAuth.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/github/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Extract and validate the JWT from the Authorization header.

    Returns the User ORM instance for the authenticated user.

    Raises:
        HTTPException 401: If the token is missing, invalid, expired,
            or the user no longer exists in the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(token)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, user_id)

    if user is None:
        raise credentials_exception

    return user
