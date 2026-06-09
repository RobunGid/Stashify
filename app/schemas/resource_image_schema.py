from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, UUID4

if TYPE_CHECKING:
    from schemas.resource_schema import ResourceSchema


class ResourceImageWithoutResourceSchema(BaseModel):
    resource_image_id: UUID4

    resource_id: UUID4
    image: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: ResourceSchema
