from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from domain.entities.base import BaseEntity
from sqlalchemy.orm import DeclarativeBase

Ent = TypeVar("Ent", bound=BaseEntity)
Mod = TypeVar("Mod", bound=DeclarativeBase)


@dataclass
class BaseMapper(ABC, Generic[Ent, Mod]):
    @staticmethod
    @abstractmethod
    def to_model(entity: Ent) -> Mod:
        pass

    @staticmethod
    @abstractmethod
    def to_entity(model: Mod) -> Ent:
        pass
