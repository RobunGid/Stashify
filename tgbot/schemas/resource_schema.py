from datetime import datetime
from typing import List

from pydantic import BaseModel


class ResourceSchema(BaseModel):
    id: str
    
    name: str
    description: str
    tags: List[str]
    verified: bool
    
    category_id: str
    category: "CategorySchema"
    
    quizes: "List[QuizSchema]"
    
    created_at: datetime
    
from .category_schema import CategorySchema
from .quiz_schema import QuizSchema