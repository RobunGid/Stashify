from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, NamedTuple, TypeVar


@dataclass
class BaseEntity(ABC):
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class BaseUpdateEntity(ABC):
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)


Ent = TypeVar("Ent", bound=BaseEntity)


class GetManyResult(Generic[Ent], NamedTuple):
    items: list[Ent]
    total: int
