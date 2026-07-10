from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class CategoryItemEntity(BaseEntity):
    category_item_id: UUID
    name: str
    resource_item_count: int


@dataclass
class CategoryItemUpdateEntity(BaseUpdateEntity):
    name: str | None
