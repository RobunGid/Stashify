from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class ResourceFavoriteFilters(BaseFilters):
    count: int | None
    user_account_id: UUID | None
