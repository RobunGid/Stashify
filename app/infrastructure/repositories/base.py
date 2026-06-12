from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

from domain.entities.base import BaseEntity, BaseUpdateEntity
from domain.filters.base import BaseFilters
from domain.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

Ent = TypeVar("Ent", bound=BaseEntity)
UpdEnt = TypeVar("UpdEnt", bound=BaseUpdateEntity)
Fils = TypeVar("Fils", bound=BaseFilters)


@dataclass
class BaseSQLAlchemyRepository(BaseRepository[Ent, UpdEnt, Fils], ABC):
    session: AsyncSession
