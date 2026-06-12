from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class CategoryItemFilters(BaseFilters):
    has_quiz_items: bool | None
    has_resource_items: bool | None
    favorite_user_id: UUID | None
