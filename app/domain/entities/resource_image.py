from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass
class ResourceImageEntity(BaseEntity):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str


@dataclass
class ResourceImageUpdateEntity(BaseEntity):
    resource_item_id: UUID | None
    image: str | None
