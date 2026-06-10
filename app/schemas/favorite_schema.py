from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FavoriteSchema(BaseModel):
    favorite_id: UUID = Field(default_factory=UUID)

    user_id: str
    user: Optional[UserSchema] = None

    resource_item_id: UUID
    resource: Optional[ResourceSchema] = Field(default=None)

    added_at: datetime = Field(default_factory=datetime.now)


from schemas.resource_schema import ResourceSchema  # noqa
from schemas.user_schema import UserSchema  # noqa
