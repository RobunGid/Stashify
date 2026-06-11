from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity


@dataclass
class BaseResourceItemRepository(ABC):
    @abstractmethod
    def get_one(self, resource_item_id: UUID) -> ResourceItemEntity:
        pass

    @abstractmethod
    def get_many(self, resource_item_id: UUID) -> list[ResourceItemEntity]:
        pass

    @abstractmethod
    def create(self, resource_item: ResourceItemEntity) -> None:
        pass

    @abstractmethod
    def delete(self, resource_item_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, resource_item_id: UUID, resource_item: ResourceItemUpdateEntity) -> None:
        pass
