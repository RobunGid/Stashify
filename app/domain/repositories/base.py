from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity, GetManyResult
from domain.filters.base import BaseFilters

Ent = TypeVar("Ent", bound=BaseEntity)
UpdEnt = TypeVar("UpdEnt", bound=BaseUpdateEntity)
Fils = TypeVar("Fils", bound=BaseFilters)


class BaseRepository(ABC, Generic[Ent, UpdEnt, Fils]):
    @abstractmethod
    async def get_one(self, item_id: UUID) -> Ent | None:
        pass

    @abstractmethod
    async def get_many(self, filters: Fils) -> GetManyResult[Ent]:
        pass

    @abstractmethod
    async def create(self, item: Ent) -> None:
        pass

    @abstractmethod
    async def delete_by_id(self, item_id: UUID) -> None:
        pass

    @abstractmethod
    async def update(self, item_id: UUID, item: UpdEnt) -> None:
        pass
