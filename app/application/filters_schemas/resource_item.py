from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.base import SortOrder
from domain.filters.resource_item import ResourceItemFilters, ResourceItemSortType
from pydantic import Field


class ResourceItemFiltersSchema(BaseFiltersSchema[ResourceItemFilters]):
    query: str | None = Field(default=None)
    category_item_id: UUID | None = Field(default=None)
    entity_cls: type[ResourceItemFilters] = ResourceItemFilters
    sort: ResourceItemSortType = "created_at"
    order: SortOrder = SortOrder.desc
    with_quiz_item: bool | None = None

    def to_entity(self) -> ResourceItemFilters:
        return ResourceItemFilters(
            count=self.count,
            offset=self.offset,
            query=self.query,
            category_item_id=self.category_item_id,
            sort=self.sort,
            order=self.order,
            with_quiz_item=self.with_quiz_item,
        )
