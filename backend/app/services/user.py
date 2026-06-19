"""User service — database CRUD operations for the User model.

Uses the repository-service pattern: this module owns all direct DB
queries for users, so endpoints never touch SQLAlchemy directly.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_github_id(db: AsyncSession, github_id: int) -> Optional[User]:
    """Find a user by their GitHub ID.

    Args:
        db: Active async database session.
        github_id: The user's GitHub numeric ID.

    Returns:
        The User if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.github_id == github_id))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """Find a user by their platform UUID.

    Args:
        db: Active async database session.
        user_id: The user's UUID (as string — will be cast).

    Returns:
        The User if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Insert a new user into the database.

    Args:
        db: Active async database session.
        user_data: Validated user creation data.

    Returns:
        The newly created User instance.
    """
    user = User(
        github_id=user_data.github_id,
        username=user_data.username,
        email=user_data.email,
        avatar_url=user_data.avatar_url,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, update_data: dict) -> User:
    """Update an existing user's fields.

    Args:
        db: Active async database session.
        user: The User instance to update.
        update_data: Dict of field names → new values.

    Returns:
        The updated User instance.
    """
    for field, value in update_data.items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def get_or_create_user(db: AsyncSession, github_data: dict) -> User:
    """Upsert a user from GitHub profile data.

    If a user with the given ``github_id`` exists, update their profile
    (username, email, avatar may change on GitHub). Otherwise create a
    new user.

    Args:
        db: Active async database session.
        github_data: Raw dict from the GitHub ``/user`` API.

    Returns:
        The existing or newly created User.
    """
    existing_user = await get_user_by_github_id(db, github_data["id"])

    if existing_user:
        # Update fields that might have changed on GitHub
        return await update_user(
            db,
            existing_user,
            {
                "username": github_data["login"],
                "email": github_data.get("email"),
                "avatar_url": github_data.get("avatar_url"),
            },
        )

    # First login — create the user
    user_data = UserCreate(
        github_id=github_data["id"],
        username=github_data["login"],
        email=github_data.get("email"),
        avatar_url=github_data.get("avatar_url"),
    )
    return await create_user(db, user_data)
