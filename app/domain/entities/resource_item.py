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

    category_id: UUID


@dataclass
class ResourceItemUpdateEntity(BaseUpdateEntity):
    name: str | None
    description: str | None
    links: str | None
    tags: str | None
    verified: bool

    category_id: UUID | None
