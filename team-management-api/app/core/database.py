from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings

# Engine manages actual database connections
# echo=True logs SQL queries (disable in production)
engine = create_async_engine( settings.DATABASE_URL, echo=True)

# Session factory:
# Creates new async DB sessions whenever application needs them
# expire_on_commit=False keeps object usable after commit
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI dependency
# Creates DB session per request and closes automatically after request completes
async def get_db():
    async with SessionLocal() as session:
        yield session