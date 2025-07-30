from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, ConfigDict

def default_category():
    return CategorySchema(id=uuid4(), name='')

class ResourceSchemaWithoutCategory(BaseModel):
    id: UUID4
    
    name: str
    description: str
    tags: str
    verified: bool = Field(default_factory=lambda: False)
    
    category_id: UUID4
    quizes: "List[QuizSchema]" = Field(default_factory=list, exclude=("resource",))
    
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True, recursive=False)

class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchema" = Field(default_factory=default_category, exclude=("resources",))
    
from .category_schema import CategorySchema
from .quiz_schema import QuizSchema