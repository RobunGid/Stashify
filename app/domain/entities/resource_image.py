from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class ResourceImageEntity(BaseEntity):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str


@dataclass
class ResourceImageUpdateEntity(BaseUpdateEntity):
    resource_item_id: UUID | None
    image: str | None
