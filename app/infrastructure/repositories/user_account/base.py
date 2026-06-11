from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseUserAccountRepository(BaseRepository, ABC):
    @abstractmethod
    def get_one(self, user_account_id: UUID) -> UserAccountEntity:
        pass

    @abstractmethod
    def get_many(self, user_account_id: UUID) -> list[UserAccountEntity]:
        pass

    @abstractmethod
    def create(self, user_account: UserAccountEntity) -> None:
        pass

    @abstractmethod
    def delete(self, user_account_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, user_account_id: UUID, user_account: UserAccountUpdateEntity) -> None:
        pass
