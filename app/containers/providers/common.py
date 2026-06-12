from typing import AsyncGenerator

from dishka import provide, Provider, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine

from settings.config import Config


class CommonProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config(**{})

    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.database_url)

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        engine: AsyncEngine,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker(engine=engine, expire_on_commit=False) as session:
            yield session
