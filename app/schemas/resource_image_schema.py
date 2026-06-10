from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, UUID


class ResourceImageWithoutResourceSchema(BaseModel):
    resource_image_id: UUID

    resource_id: UUID
    image: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: ResourceSchema


from schemas.resource_schema import ResourceSchema  # noqa
