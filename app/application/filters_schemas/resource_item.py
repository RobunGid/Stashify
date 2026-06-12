from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.resource_item import ResourceItemFilters
from pydantic import Field


class ResourceItemFiltersSchema(BaseFiltersSchema[ResourceItemFilters]):
    text: str | None = Field(default=None)
    category_item_id: UUID | None = Field(default=None)
    entity_cls: type[ResourceItemFilters] = ResourceItemFilters

    def to_entity(self) -> ResourceItemFilters:
        return ResourceItemFilters(
            count=self.count,
            offset=self.offset,
            text=self.text,
            category_item_id=self.category_item_id,
        )
