from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class ResourceFavoriteFilters(BaseFilters):
    user_account_id: UUID | None = None
