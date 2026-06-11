from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResourceRatingWithoutUserAndResourceSchema(BaseModel):
    resource_rating_id: UUID

    resource_item_id: UUID

    user_id: str

    created_at: datetime
    rating: int
    model_config = ConfigDict(from_attributes=True)


class ResourceRatingSchema(ResourceRatingWithoutUserAndResourceSchema):
    user: PlainUserSchema
    resource: ResourceItemSchema


from application.schemas.resource_schema import ResourceItemSchema  # noqa
from application.schemas.user_schema import PlainUserSchema  # noqa
