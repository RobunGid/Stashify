from abc import ABC

from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from domain.filters.user_account import UserAccountFilters
from infrastructure.repositories.base import BaseRepository


class BaseUserAccountRepository(BaseRepository[UserAccountEntity, UserAccountUpdateEntity, UserAccountFilters], ABC):
    pass
