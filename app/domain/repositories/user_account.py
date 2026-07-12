from abc import ABC, abstractmethod

from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from domain.filters.user_account import UserAccountFilters
from domain.repositories.base import BaseRepository


class BaseUserAccountRepository(BaseRepository[UserAccountEntity, UserAccountUpdateEntity, UserAccountFilters], ABC):
    @abstractmethod
    async def get_one_by_telegram_id(self, telegram_id: int) -> UserAccountEntity | None:
        pass
