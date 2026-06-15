from uuid import UUID

from application.services.base import BaseService
from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from domain.repositories.resource_item import BaseResourceItemRepository


class ResourceItemService(BaseService[ResourceItemEntity, ResourceItemUpdateEntity, ResourceItemFilters]):
    repository: BaseResourceItemRepository

    async def get_one_by_filters(self, filters: ResourceItemFilters) -> ResourceItemEntity | None:
        if filters.offset < 0:
            return None
        resource_item_entities, _ = await self.repository.get_many(filters)
        return resource_item_entities[0] if len(resource_item_entities) else None

    async def get_resource_item_index_in_category(
        self,
        resource_item_id: UUID,
        filters: ResourceItemFilters,
    ) -> int | None:
        return await self.repository.get_resource_item_index_in_category(resource_item_id, filters)
