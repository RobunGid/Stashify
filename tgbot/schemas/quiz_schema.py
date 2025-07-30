from typing import List

from pydantic import BaseModel, Field, ConfigDict

class QuizSchema(BaseModel):
    id: str = Field()
    
    resource_id: str
    resource: "ResourceSchema"
    
    questions: "List[QuizQuestionSchema]" = Field(exclude=("quiz",))
    
    model_config = ConfigDict(from_attributes=True, recursive=False)
    
from .resource_schema import ResourceSchema
from .quiz_question_schema import QuizQuestionSchema