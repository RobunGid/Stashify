from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

type BaseSortType = Literal["created_at"] | Literal["updated_at"]


class SortOrder(Enum):
    desc = "desc"
    asc = "asc"


@dataclass
class BaseFilters:
    count: int | None = None
    offset: int = field(default=0, kw_only=True)
    order: SortOrder = field(default=SortOrder.asc, kw_only=True)
    sort: BaseSortType = field(default="created_at", kw_only=True)
