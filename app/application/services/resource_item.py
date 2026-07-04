from uuid import UUID

from application.exceptions.resource_item import ResourceItemNotFoundException
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

    async def get_resource_pagination(self, category_item_id: UUID, resource_item_id: UUID):
        filters = ResourceItemFilters(
            count=1,
            category_item_id=category_item_id,
        )

        index = await self.get_resource_item_index_in_category(resource_item_id, filters)

        if index is None:
            raise ResourceItemNotFoundException(resource_item_id)

        total_count = await self.get_count(
            ResourceItemFilters(
                category_item_id=category_item_id,
                count=0,
            ),
        )

        prev_id: UUID | None = None
        next_id: UUID | None = None

        if index > 0:
            prev_entity = await self.get_one_by_filters(
                ResourceItemFilters(
                    count=1,
                    offset=index - 1,
                    category_item_id=category_item_id,
                ),
            )
            prev_id = getattr(prev_entity, "resource_item_id", None)

        if index < total_count - 1:
            next_entity = await self.get_one_by_filters(
                ResourceItemFilters(
                    count=1,
                    offset=index + 1,
                    category_item_id=category_item_id,
                ),
            )
            next_id = getattr(next_entity, "resource_item_id", None)

        first_id: UUID | None = None
        last_id: UUID | None = None

        if total_count > 0 and index != 0:
            first_entity = await self.get_one_by_filters(
                ResourceItemFilters(
                    count=1,
                    offset=0,
                    category_item_id=category_item_id,
                ),
            )
            first_id = getattr(first_entity, "resource_item_id", None)

        if total_count > 0 and index != total_count - 1:
            last_entity = await self.get_one_by_filters(
                ResourceItemFilters(
                    count=1,
                    offset=total_count - 1,
                    category_item_id=category_item_id,
                ),
            )
            last_id = getattr(last_entity, "resource_item_id", None)

        return (
            index,
            (first_id, prev_id, next_id, last_id),
            total_count,
        )
