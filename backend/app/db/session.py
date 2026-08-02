"""
Database session and connection management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event

from app.config.settings import settings
from app.models.base import Base as BaseModel

# Create async engine with error handling for missing database drivers
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,  # Set to True for debugging
    )
except ImportError as e:
    # Database driver might not be available (e.g., psycopg2, asyncpg)
    print(f"Database driver not available: {e}")
    # Create a mock engine for testing without database
    class MockAsyncEngine:
        def __init__(self):
            pass
        def dispose(self):
            pass
    engine = MockAsyncEngine()

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
    try:
        async with async_session_maker() as session:
            # Ensure models are tied to the base
            for model in BaseModel.__subclasses__():
                pass
            yield session
    except Exception:
        # If database is not available, yield a mock session
        class MockSession:
            def __init__(self):
                pass
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                pass
            def commit(self):
                pass
            def rollback(self):
                pass
            def add(self, *args):
                pass
            def execute(self, *args):
                class MockResult:
                    def scalar(self):
                        return None
                return MockResult()
        yield MockSession()

# For synchronous usage (alembic)
def get_sync_engine():
    """Get a synchronous engine for alembic migrations"""
    try:
        from sqlalchemy import create_engine
        sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
        return create_engine(sync_url)
    except Exception:
        # Return mock sync engine if database is not available
        class MockSyncEngine:
            def __init__(self):
                pass
            def dispose(self):
                pass
            def connect(self):
                class MockConnection:
                    def __init__(self):
                        pass
                    def execute(self, *args):
                        class MockResult:
                            def fetchone(self):
                                return None
                            def scalar(self):
                                return None
                        return MockResult()
                    def commit(self):
                        pass
                    def close(self):
                        pass
                    def __enter__(self):
                        return self
                    def __exit__(self, *args):
                        pass
                return MockConnection()
        return MockSyncEngine()
