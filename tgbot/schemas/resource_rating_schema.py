from datetime import datetime

from pydantic import UUID4, BaseModel, Field, ConfigDict

class ResourceRatingWithoutUserAndResourceSchema(BaseModel):
    id: UUID4
    
    resource_id: UUID4
    
    user_id: str
    
    created_at: datetime = Field(default_factory=datetime.now)
    rating: int
    model_config = ConfigDict(from_attributes=True)
    
class ResourceRatingSchema(ResourceRatingWithoutUserAndResourceSchema):
    user: "UserSchema"
    resource: "ResourceSchema"
    
from .user_schema import UserSchema
from .resource_schema import ResourceSchema