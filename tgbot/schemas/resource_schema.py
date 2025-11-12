from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, ConfigDict

from utils.OptionalSchema import AllOptional

def default_category():
    return CategorySchemaWithoutResources(id=uuid4(), name='')

class ResourceSchemaWithoutCategory(BaseModel):
    id: UUID4
    
    name: str
    description: str
    links: str
    tags: str
    verified: bool = Field(default_factory=lambda: False)
    image: str
    
    category_id: UUID4
    quiz: Optional["QuizSchemaWithoutResource"] = Field(default_factory=lambda: None)
    
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)

class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchemaWithoutResources" = Field(default_factory=default_category)
    ratings: List["ResourceRatingWithoutUserAndResourceSchema"] = Field(default_factory=list)
    
class UpdateResourceSchemaWithoutCategory(ResourceSchemaWithoutCategory, metaclass=AllOptional):
    ...
    
from .category_schema import CategorySchemaWithoutResources
from .quiz_schema import QuizSchemaWithoutResource
from .resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema