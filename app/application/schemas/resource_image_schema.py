from __future__ import annotations

from uuid import UUID

from application.schemas.base_schema import BaseSchema
from pydantic import ConfigDict


class ResourceImageWithoutResourceSchema(BaseSchema):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str

    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: ResourceItemSchema


from application.schemas.resource_schema import ResourceItemSchema  # noqa
