from typing import Optional
from uuid import UUID

from pydantic import Field
from application.schemas.base_schema import BaseSchema


class ResourceFavoriteSchema(BaseSchema):
    favorite_id: UUID = Field(default_factory=UUID)

    user_id: str
    user: Optional[UserAccountSchema] = None

    resource_item_id: UUID
    resource: Optional[ResourceItemSchema] = Field(default=None)


from application.schemas.resource_schema import ResourceItemSchema  # noqa
from application.schemas.user_account_schema import UserAccountSchema  # noqa
