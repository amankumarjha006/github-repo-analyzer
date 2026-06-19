"""Pydantic schemas for User request/response validation.

These schemas are the contract between the API and the outside world.
They are intentionally separate from the SQLAlchemy model to keep
the ORM layer decoupled from the HTTP layer.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Base ──────────────────────────────────────────────────────────────────
class UserBase(BaseModel):
    """Fields shared across create/read/update schemas."""

    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None


# ── Create ────────────────────────────────────────────────────────────────
class UserCreate(UserBase):
    """Data required to create a new user (from GitHub OAuth)."""

    github_id: int


# ── Update ────────────────────────────────────────────────────────────────
class UserUpdate(BaseModel):
    """Optional fields that can be patched on an existing user."""

    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None


# ── Read (response) ──────────────────────────────────────────────────────
class UserRead(UserBase):
    """Schema returned by the API — includes id and timestamps."""

    id: uuid.UUID
    github_id: int
    created_at: datetime
    updated_at: datetime

    # Allow reading attributes directly from SQLAlchemy model instances.
    model_config = ConfigDict(from_attributes=True)
