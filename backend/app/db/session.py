"""Async database engine and session factory.

Uses psycopg3 as the async PostgreSQL driver (works on Python 3.14 without
a C compiler, unlike asyncpg).

DATABASE_URL format: ``postgresql+psycopg://user:pass@host/db?sslmode=require``

Provides:
    - ``async_engine``: the SQLAlchemy async engine bound to Neon.
    - ``AsyncSessionLocal``: session factory for creating async sessions.
    - ``get_db()``: FastAPI dependency that yields a session per request.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# ── Engine ────────────────────────────────────────────────────────────────
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True to log every SQL statement (noisy but useful for debugging)
    pool_pre_ping=True,  # Detect stale connections before using them
)

# ── Session Factory ───────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── FastAPI Dependency ────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session and ensure it is closed after the request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
