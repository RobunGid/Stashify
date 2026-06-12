from application.containers.factories import get_container
from sqlalchemy.ext.asyncio import AsyncEngine

from database.base import Base


async def init_models():
    container = get_container()
    async with container() as request_container:
        engine = await request_container.get(AsyncEngine)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
