from typing import List

from pydantic import BaseModel, Field, ConfigDict

class QuizSchemaWithoutResource(BaseModel):
    id: str = Field()
    
    resource_id: str
    
    questions: "List[QuizQuestionSchema]"
    
    model_config = ConfigDict(from_attributes=True)
    
class QuizSchema(QuizSchemaWithoutResource):
    resource: "ResourceSchema"
    
from .resource_schema import ResourceSchema
from .quiz_question_schema import QuizQuestionSchema