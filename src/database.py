from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.settings import settings as s
from src.models.models import Base

DATABASE_URL = f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"

async_engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# async def init_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)