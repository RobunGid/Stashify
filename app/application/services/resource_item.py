from typing import cast
from uuid import UUID

from application.exceptions.resource_item import ResourceItemNotFoundException
from application.services.base import BaseService
from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.base import SortOrder
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
        current_resource_item_filter_schema = ResourceItemFilters(
            count=1,
            category_item_id=category_item_id,
        )

        resource_item_index_in_category = await self.get_resource_item_index_in_category(
            resource_item_id,
            current_resource_item_filter_schema,
        )
        if resource_item_index_in_category is None:
            raise ResourceItemNotFoundException(resource_item_id)

        first_resource_item_filter_schema = ResourceItemFilters(
            count=1,
            category_item_id=category_item_id,
        )

        previous_resource_item_filter_schema = ResourceItemFilters(
            count=1,
            offset=resource_item_index_in_category - 1,
            category_item_id=category_item_id,
        )

        next_resource_item_filter_schema = ResourceItemFilters(
            count=1,
            offset=resource_item_index_in_category + 1,
            category_item_id=category_item_id,
        )

        last_resource_item_filter_schema = ResourceItemFilters(
            count=1,
            category_item_id=category_item_id,
            order=SortOrder.asc if first_resource_item_filter_schema.order == SortOrder.desc else SortOrder.desc,
        )

        first_resource_item_entity = await self.get_one_by_filters(
            filters=first_resource_item_filter_schema,
        )
        previous_resource_item_entity = await self.get_one_by_filters(
            filters=previous_resource_item_filter_schema,
        )
        next_resource_item_entity = await self.get_one_by_filters(
            filters=next_resource_item_filter_schema,
        )

        last_resource_item_entity = await self.get_one_by_filters(
            filters=last_resource_item_filter_schema,
        )

        resource_item_entities_navigation_tuple = (
            first_resource_item_entity,
            previous_resource_item_entity,
            next_resource_item_entity,
            last_resource_item_entity,
        )

        resource_item_entities_navigation_ids_tuple = cast(
            tuple[UUID | None, UUID | None, UUID | None, UUID | None],
            tuple(
                getattr(resource_item_entity, "resource_item_id", None)
                for resource_item_entity in resource_item_entities_navigation_tuple
            ),
        )
        resource_item_count_filters = ResourceItemFilters(
            category_item_id=category_item_id,
            count=0,
        )
        total_resource_item_count = await self.get_count(resource_item_count_filters)

        return (
            resource_item_index_in_category,
            resource_item_entities_navigation_ids_tuple,
            total_resource_item_count,
        )
