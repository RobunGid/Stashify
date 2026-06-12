from abc import abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

from domain.entities.base import BaseEntity, BaseUpdateEntity
from pydantic import BaseModel, Field

Ent = TypeVar("Ent", bound=BaseEntity)
UpdEnt = TypeVar("UpdEnt", bound=BaseUpdateEntity)


class BaseSchema(BaseModel, Generic[Ent]):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @abstractmethod
    def to_entity(self) -> Ent:
        pass


class BaseUpdateSchema(BaseModel, Generic[UpdEnt]):
    updated_at: datetime = Field(default_factory=datetime.now)

    @abstractmethod
    def to_entity(self) -> UpdEnt:
        pass
