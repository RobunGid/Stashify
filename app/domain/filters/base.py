from dataclasses import dataclass


@dataclass
class BaseFilters:
    count: int
    offset: int
