from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from domain.repositories.base import BaseRepository


class BaseResourceItemRepository(
    BaseRepository[ResourceItemEntity, ResourceItemUpdateEntity, ResourceItemFilters],
    ABC,
):
    @abstractmethod
    async def get_index_in_category(self, resource_item_id: UUID, category_item_id: UUID) -> int | None:
        pass
