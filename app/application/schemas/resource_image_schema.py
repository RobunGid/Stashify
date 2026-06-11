from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResourceImageWithoutResourceSchema(BaseModel):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str

    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: ResourceItemSchema


from application.schemas.resource_schema import ResourceItemSchema  # noqa
