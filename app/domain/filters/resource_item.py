from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from domain.filters.base import BaseFilters, BaseSortType, SortOrder

type ResourceItemSortType = BaseSortType | Literal["name"]


@dataclass
class ResourceItemFilters(BaseFilters):
    query: str | None = None
    category_item_id: UUID | None = None
    sort: ResourceItemSortType = "created_at"
    order: SortOrder = SortOrder.desc
