from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema


class CategoryItemFiltersSchema(BaseFiltersSchema):
    has_quiz_items: bool
    has_resource_items: bool
    favorite_user_id: UUID
