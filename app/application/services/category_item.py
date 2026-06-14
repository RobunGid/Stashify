from uuid import UUID

from application.services.base import BaseService
from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from domain.repositories.category_item import BaseCategoryItemRepository


class CategoryItemService(BaseService[CategoryItemEntity, CategoryItemUpdateEntity, CategoryItemFilters]):
    repository: BaseCategoryItemRepository

    async def get_resource_item_index_in_category(self, resource_item_id: UUID, category_item_id: UUID) -> int | None:
        return await self.repository.get_resource_item_index_in_category(resource_item_id, category_item_id)
