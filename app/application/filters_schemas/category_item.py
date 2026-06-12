from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.category_item import CategoryItemFilters


class CategoryItemFiltersSchema(BaseFiltersSchema):
    has_quiz_items: bool
    has_resource_items: bool = False
    favorite_user_id: UUID | None = None
    entity_cls: type[CategoryItemFilters] = CategoryItemFilters
