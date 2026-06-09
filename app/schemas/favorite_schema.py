from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4

from schemas.resource_schema import ResourceSchema
from schemas.user_schema import UserSchema


class FavoriteSchema(BaseModel):
    favorite_id: UUID4 = Field(default_factory=uuid4)

    user_id: str
    user: Optional["UserSchema"] = None

    resource_id: UUID4
    resource: Optional["ResourceSchema"] = Field(default_factory=lambda: None)

    added_at: datetime = Field(default_factory=datetime.now)
