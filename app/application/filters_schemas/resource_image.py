from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.resource_image import ResourceImageFilters


class ResourceImageFiltersSchema(BaseFiltersSchema[ResourceImageFilters]):
    resource_item_id: UUID | None = None
    count: int | None = None

    entity_cls: type[ResourceImageFilters] = ResourceImageFilters

    def to_entity(self) -> ResourceImageFilters:
        return ResourceImageFilters(count=self.count, offset=self.offset, resource_item_id=self.resource_item_id)
