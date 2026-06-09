from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, UUID4


class ResourceImageWithoutResourceSchema(BaseModel):
    id: UUID4

    resource_id: UUID4
    image: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceImageSchema(ResourceImageWithoutResourceSchema):
    resource: "ResourceSchema"


from .resource_schema import ResourceSchema
