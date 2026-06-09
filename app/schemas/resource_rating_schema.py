from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, UUID4


class ResourceRatingWithoutUserAndResourceSchema(BaseModel):
    resource_rating_id: UUID4

    resource_id: UUID4

    user_id: str

    created_at: datetime = Field(default_factory=datetime.now)
    rating: int
    model_config = ConfigDict(from_attributes=True)


class ResourceRatingSchema(ResourceRatingWithoutUserAndResourceSchema):
    user: PlainUserSchema
    resource: ResourceSchema


from schemas.user_schema import PlainUserSchema
from schemas.resource_schema import ResourceSchema
