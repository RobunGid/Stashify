from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ResourceFavoriteSchema(BaseModel):
    favorite_id: UUID = Field(default_factory=UUID)

    user_id: str
    user: Optional[UserSchema] = None

    resource_item_id: UUID
    resource: Optional[ResourceItemSchema] = Field(default=None)

    added_at: datetime


from application.schemas.resource_schema import ResourceItemSchema  # noqa
from application.schemas.user_schema import UserSchema  # noqa
