"""User endpoints — current user profile.

Routes:
    GET /me → Returns the authenticated user's profile.
"""

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Return the profile of the currently authenticated user.

    This is a **protected route** — requires a valid access token
    in the ``Authorization: Bearer <token>`` header.
    """
    return current_user
