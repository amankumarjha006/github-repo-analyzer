"""API v1 router — aggregates all endpoint routers under /api/v1.

Import this single router in main.py to mount all versioned endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
