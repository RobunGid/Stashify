from typing import AsyncGenerator

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from application.services.category_item import CategoryItemService
from dishka import AnyOf, provide, Provider, Scope
from infrastructure.repositories.category_item.base import BaseCategoryItemRepository
from infrastructure.repositories.category_item.sql import SQLCategoryItemRepository
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine

from settings.config import Config


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config(**{})

    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.database_url)

    @provide(scope=Scope.APP)
    def пуе_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        engine: AsyncEngine,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_category_items_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseCategoryItemRepository, SQLCategoryItemRepository]:
        return SQLCategoryItemRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_chats_service(self, repository: BaseCategoryItemRepository) -> CategoryItemService:
        return CategoryItemService(repository=repository)

    @provide(scope=Scope.APP)
    def get_bot(self, config: Config) -> Bot:
        return Bot(
            config.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    @provide(scope=Scope.APP)
    def get_aiogram_storage(self) -> AnyOf[BaseStorage, MemoryStorage]:
        return MemoryStorage()

    @provide(scope=Scope.APP)
    def get_aiogram_dispatcher(self, storage: BaseStorage):
        return Dispatcher(storage=storage, echo=True)
