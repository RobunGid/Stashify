from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class ResourceItemFilters(BaseFilters):
    text: str | None
    category_item_id: UUID | None
