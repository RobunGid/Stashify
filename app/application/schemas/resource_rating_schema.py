from uuid import UUID

from application.schemas.base_schema import BaseSchema
from pydantic import ConfigDict


class ResourceRatingWithoutUserAndResourceSchema(BaseSchema):
    resource_rating_id: UUID

    resource_item_id: UUID

    user_id: str

    rating: int
    model_config = ConfigDict(from_attributes=True)


class ResourceRatingSchema(ResourceRatingWithoutUserAndResourceSchema):
    user: PlainUserAccountSchema
    resource: ResourceItemSchema


from application.schemas.resource_schema import ResourceItemSchema  # noqa
from application.schemas.user_account_schema import PlainUserAccountSchema  # noqa
