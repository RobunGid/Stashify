from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class ResourceImageFilters(BaseFilters):
    resource_item_id: UUID | None = None
    count: int | None = None
