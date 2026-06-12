from typing import Generic, Type, TypeVar

from domain.filters.base import BaseFilters
from pydantic import BaseModel

Fils = TypeVar("Fils", bound=BaseFilters)


class BaseFiltersSchema(BaseModel, Generic[Fils]):
    count: int
    offset: int = 0
    entity_cls: Type[Fils]

    def to_entity(self) -> Fils:
        return self.entity_cls(**self.model_dump(exclude_none=True))
