from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class ResourceItemEntity(BaseEntity):
    resource_item_id: UUID

    name: str
    description: str
    links: str
    tags: str
    verified: bool

    category_item_id: UUID


@dataclass
class ResourceItemUpdateEntity(BaseUpdateEntity):
    name: str | None = None
    description: str | None = None
    links: str | None = None
    tags: str | None = None
    verified: bool | None = None

    category_item_id: UUID | None = None
