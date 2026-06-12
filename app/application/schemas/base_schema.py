from abc import abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

from domain.entities.base import BaseEntity
from pydantic import BaseModel, Field

Ent = TypeVar("Ent", bound=BaseEntity)


class BaseSchema(BaseModel, Generic[Ent]):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @abstractmethod
    def to_entity(self) -> Ent:
        pass
