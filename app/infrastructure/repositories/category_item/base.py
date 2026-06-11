from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity


@dataclass
class BaseCategoryItemRepository(ABC):
    @abstractmethod
    def get_one(self, category_item_id: UUID) -> CategoryItemEntity:
        pass

    @abstractmethod
    def get_many(self, category_item_id: UUID) -> list[CategoryItemEntity]:
        pass

    @abstractmethod
    def create(self, category_item: CategoryItemEntity) -> None:
        pass

    @abstractmethod
    def delete(self, category_item_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, category_item_id: UUID, category_item: CategoryItemUpdateEntity) -> None:
        pass
