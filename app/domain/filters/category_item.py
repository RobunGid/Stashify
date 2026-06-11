from uuid import UUID

from domain.filters.base import BaseFilters


class CategoryItemFilters(BaseFilters):
    has_quiz_items: bool
    has_resource_items: bool
    favorite_user_id: UUID
