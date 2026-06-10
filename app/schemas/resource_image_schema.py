from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ResourceImageWithoutResourceSchema(BaseModel):
    resource_image_id: UUID

    resource_item_id: UUID
    image: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: ResourceItemSchema


from schemas.resource_schema import ResourceItemSchema  # noqa
