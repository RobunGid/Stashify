from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.resource_rating import ResourceRatingEntity
from pydantic import ConfigDict


class BaseResourceRatingSchema(BaseSchema[ResourceRatingEntity]):
    resource_rating_id: UUID
    resource_item_id: UUID
    user_account_id: UUID
    rating: int

    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> ResourceRatingEntity:
        return ResourceRatingEntity(
            resource_rating_id=self.resource_rating_id,
            resource_item_id=self.resource_item_id,
            user_account_id=self.user_account_id,
            rating=self.rating,
        )


class ResourceRatingSchema(BaseResourceRatingSchema):
    user: BaseUserAccountSchema
    resource: ResourceItemSchema


from application.schemas.resource_item_schema import ResourceItemSchema  # noqa
from application.schemas.user_account_schema import BaseUserAccountSchema  # noqa
