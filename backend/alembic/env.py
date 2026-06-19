"""Alembic environment configuration for async PostgreSQL migrations.

This replaces the default sync env.py with an async-compatible version
that uses our app's settings and SQLAlchemy Base metadata.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ── App imports ───────────────────────────────────────────────────────────
# Import all models here so that Base.metadata is populated before
# Alembic tries to autogenerate migrations.
from app.core.config import settings
from app.db.base import Base
from app.models.user import User  # noqa: F401 — needed for autogenerate

# ── Alembic Config ────────────────────────────────────────────────────────
config = context.config

# Override the sqlalchemy.url from alembic.ini with our app's DATABASE_URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the metadata Alembic uses to detect schema changes
target_metadata = Base.metadata


# ── Offline Mode (SQL script generation) ──────────────────────────────────
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generates SQL without connecting."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online Mode (async) ──────────────────────────────────────────────────
def do_run_migrations(connection) -> None:
    """Configure context with the connection and run migrations."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations inside a connection."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode — connects to the live database."""
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_async_migrations())


# ── Entry point ───────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
