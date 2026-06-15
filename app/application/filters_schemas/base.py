from abc import abstractmethod
from typing import Generic, Type, TypeVar

from domain.filters.base import BaseFilters, BaseSortType, SortOrder
from pydantic import BaseModel

Fils = TypeVar("Fils", bound=BaseFilters)


class BaseFiltersSchema(BaseModel, Generic[Fils]):
    count: int
    offset: int = 0
    sort: BaseSortType = "created_at"
    order: SortOrder = SortOrder.asc
    entity_cls: Type[Fils]

    @abstractmethod
    def to_entity(self) -> Fils:
        pass
