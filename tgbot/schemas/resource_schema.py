from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, ConfigDict

def default_category():
    return CategorySchemaWithoutResources(id=uuid4(), name='')

class ResourceSchemaWithoutCategory(BaseModel):
    id: UUID4
    
    name: str
    description: str
    tags: str
    verified: bool = Field(default_factory=lambda: False)
    image: str
    
    category_id: UUID4
    quizes: "List[QuizSchema]" = Field(default_factory=lambda: [])
    
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)

class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchemaWithoutResources" = Field(default_factory=default_category)
    
from .category_schema import CategorySchemaWithoutResources
from .quiz_schema import QuizSchema