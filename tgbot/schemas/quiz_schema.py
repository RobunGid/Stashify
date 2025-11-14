from typing import List

from pydantic import BaseModel, Field, ConfigDict, UUID4

class PlainQuizSchema(BaseModel):
    id: UUID4 = Field()
    
    resource_id: UUID4
    
    model_config = ConfigDict(from_attributes=True)
    
class QuizSchemaWithoutResource(PlainQuizSchema):
    questions: "List[QuizQuestionBaseSchema]" = Field(default_factory=list)
    
class QuizSchema(QuizSchemaWithoutResource):
    resource: "ResourceSchema"
    
from .resource_schema import ResourceSchema
from .quiz_question_schema import QuizQuestionBaseSchema