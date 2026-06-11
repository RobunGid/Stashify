from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, NamedTuple, TypeVar


class BaseEntity(ABC):
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)


Ent = TypeVar("Ent", bound=BaseEntity)


@dataclass()
class GetManyResult(Generic[Ent], NamedTuple):
    items: list[Ent]
    total: int
