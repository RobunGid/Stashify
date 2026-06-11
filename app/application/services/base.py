from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.filters.base import BaseFilters
from infrastructure.repositories.base import BaseRepository

Ent = TypeVar("Ent", bound=BaseEntity)
UpdEnt = TypeVar("UpdEnt", bound=BaseEntity)
Fils = TypeVar("Fils", bound=BaseFilters)


@dataclass
class BaseService(ABC, Generic[Ent, UpdEnt, Fils]):
    repository: BaseRepository[Ent, UpdEnt, Fils]

    async def get_one(self, item_id: UUID) -> Ent | None:
        return await self.repository.get_one(item_id)

    async def get_many(self, filters: Fils) -> list[Ent]:
        return await self.repository.get_many(filters)

    async def create(self, item: Ent) -> None:
        return await self.repository.create(item)

    async def delete(self, item_id: UUID) -> None:
        return await self.repository.delete(item_id)

    async def update(self, item_id: UUID, item: UpdEnt) -> None:
        return await self.repository.update(item_id, item)
