from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseResourceImageRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_one(self, resource_image_id: UUID) -> ResourceImageEntity | None:
        pass

    @abstractmethod
    async def get_many(self, resource_image_id: UUID) -> list[ResourceImageEntity]:
        pass

    @abstractmethod
    async def create(self, resource_image: ResourceImageEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, resource_image_id: UUID) -> None:
        pass

    @abstractmethod
    async def update(self, resource_image_id: UUID, resource_image: ResourceImageUpdateEntity) -> None:
        pass
