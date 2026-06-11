from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity


@dataclass
class BaseResourceImageRepository(ABC):
    @abstractmethod
    def get_one(self, resource_image_id: UUID) -> ResourceImageEntity:
        pass

    @abstractmethod
    def get_many(self, resource_image_id: UUID) -> list[ResourceImageEntity]:
        pass

    @abstractmethod
    def create(self, resource_image: ResourceImageEntity) -> None:
        pass

    @abstractmethod
    def delete(self, resource_image_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, resource_image_id: UUID, resource_image: ResourceImageUpdateEntity) -> None:
        pass
