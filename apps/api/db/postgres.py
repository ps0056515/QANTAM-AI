"""
PostgreSQL Connection - Operational database connection management
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://qantam:qantam@localhost:5432/qantam"
)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    """Get database session as dependency."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
