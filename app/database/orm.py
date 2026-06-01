from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from settings.config import config

Base = declarative_base()
engine = create_async_engine(config.database_url)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=True, class_=AsyncSession)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)