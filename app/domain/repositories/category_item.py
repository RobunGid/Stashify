from abc import abstractmethod
from uuid import UUID

from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from domain.repositories.base import BaseRepository


class BaseCategoryItemRepository(BaseRepository[CategoryItemEntity, CategoryItemUpdateEntity, CategoryItemFilters]):
    @abstractmethod
    async def get_resource_item_index_in_category(self, resource_item_id: UUID, category_item_id: UUID) -> int | None:
        pass
