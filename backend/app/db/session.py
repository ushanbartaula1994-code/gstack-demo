"""
Database session and connection management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event

from app.config.settings import settings
from app.models.base import Base as BaseModel

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for debugging
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Base for all models
Base = declarative_base()


# Dependency for FastAPI
async def get_db():
    """Dependency that provides a database session"""
    async with async_session_maker() as session:
        # Ensure models are tied to the base
        for model in BaseModel.__subclasses__():
            pass
        yield session


# For synchronous usage (alembic)
def get_sync_engine():
    """Get a synchronous engine for alembic migrations"""
    from sqlalchemy import create_engine
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    return create_engine(sync_url)
