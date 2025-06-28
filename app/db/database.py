# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session