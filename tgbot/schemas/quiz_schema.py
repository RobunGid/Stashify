from typing import List

from pydantic import BaseModel, Field

class QuizSchema(BaseModel):
    id: str = Field()
    
    resource_id: str
    resource: "ResourceSchema"
    
    questions: "List[QuizQuestionSchema]"
    
from .resource_schema import ResourceSchema
from .quiz_question_schema import QuizQuestionSchema