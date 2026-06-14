from dataclasses import dataclass, field


@dataclass
class BaseFilters:
    count: int
    offset: int = field(default=0, kw_only=True)
