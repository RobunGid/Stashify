from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.resource_favorite import ResourceFavoriteEntity
from pydantic import Field


class BaseResourceFavoriteSchema(BaseSchema[ResourceFavoriteEntity]):
    resource_favorite_id: UUID = Field(default_factory=UUID)

    user_account_id: UUID

    resource_item_id: UUID

    def to_entity(self) -> ResourceFavoriteEntity:
        return ResourceFavoriteEntity(
            resource_favorite_id=self.resource_favorite_id,
            user_account_id=self.user_account_id,
            resource_item_id=self.resource_item_id,
        )


class ResourceFavoriteSchema(BaseResourceFavoriteSchema):
    user_account: UserAccountSchema
    resource_item: ResourceItemSchema


from application.schemas.resource_item_schema import ResourceItemSchema  # noqa
from application.schemas.user_account_schema import UserAccountSchema  # noqa
