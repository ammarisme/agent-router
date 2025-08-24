"""Database session configuration."""

import asyncio
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.db.models import Base

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def configure_database() -> None:
    """Configure database with SQLite WAL mode and other optimizations."""
    if "sqlite" in settings.database_url:
        async with engine.begin() as conn:
            # Enable WAL mode for better concurrency
            await conn.execute(text("PRAGMA journal_mode=WAL"))
            # Set busy timeout
            await conn.execute(text("PRAGMA busy_timeout=5000"))
            # Enable foreign keys
            await conn.execute(text("PRAGMA foreign_keys=ON"))
            # Set cache size
            await conn.execute(text("PRAGMA cache_size=10000"))
            # Set temp store to memory
            await conn.execute(text("PRAGMA temp_store=MEMORY"))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()