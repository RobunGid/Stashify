from typing import Optional
from datetime import datetime
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

class FavoriteSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    
    user_id: str
    user: Optional["UserSchema"] = None
    
    resource_id: UUID4
    resource: Optional["ResourceSchema"] = Field(default_factory=lambda: None)
    
    added_at: datetime = Field(default_factory=datetime.now)
    
from .user_schema import UserSchema
from .resource_schema import ResourceSchema