"""GitHub Intelligence Platform — FastAPI application entry point.

Configures CORS, mounts the versioned API router, and exposes a
/health endpoint for infrastructure checks.
"""

import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.db import base  # noqa: F401

app = FastAPI(
    title="GitHub Intelligence Platform",
    description="Analyze GitHub repositories with intelligence.",
    version="0.1.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routes ────────────────────────────────────────────────────────────
app.include_router(v1_router)


# ── Health Check ──────────────────────────────────────────────────────────
@app.get("/health")
def health():
    """Infrastructure health check — returns 200 if the service is alive."""
    return {"status": "healthy"}