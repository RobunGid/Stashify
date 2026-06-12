from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.category_item import CategoryItemFilters


class CategoryItemFiltersSchema(BaseFiltersSchema[CategoryItemFilters]):
    has_quiz_items: bool = False
    has_resource_items: bool = False
    favorite_user_id: UUID | None = None
    entity_cls: type[CategoryItemFilters] = CategoryItemFilters

    def to_entity(self) -> CategoryItemFilters:
        return CategoryItemFilters(
            count=self.count,
            offset=self.offset,
            has_quiz_items=self.has_quiz_items,
            has_resource_items=self.has_resource_items,
            favorite_user_id=self.favorite_user_id,
        )
