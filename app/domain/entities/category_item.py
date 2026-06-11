from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass
class CategoryItemEntity(BaseEntity):
    category_item_id: UUID
    name: str


@dataclass
class CategoryItemUpdateEntity(BaseEntity):
    name: str | None
