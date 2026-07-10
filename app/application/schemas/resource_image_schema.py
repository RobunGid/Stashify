from __future__ import annotations

from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.resource_image import ResourceImageEntity
from pydantic import ConfigDict


class BaseResourceImageSchema(BaseSchema[ResourceImageEntity]):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str

    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> ResourceImageEntity:
        return ResourceImageEntity(
            resource_image_id=self.resource_image_id,
            resource_item_id=self.resource_item_id,
            image=self.image,
        )


class ResourceImageSchema(BaseResourceImageSchema):
    resource: ResourceItemSchema


from application.schemas.resource_item_schema import ResourceItemSchema  # noqa
