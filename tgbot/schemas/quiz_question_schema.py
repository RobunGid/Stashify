
from typing import List, Optional

from pydantic import BaseModel, UUID4, ConfigDict

class QuizQuestionBaseSchema(BaseModel):
    id: UUID4
    text: str
    
    quiz_id: UUID4
    
    options: List[str]
    right_options: List[int]
    
    image: Optional[str]
    model_config = ConfigDict(from_attributes=True)
    
class QuizQuestionSchema(QuizQuestionBaseSchema):
    quiz: "QuizSchema"

class QuizQuestionWithoutResourceSchema(QuizQuestionBaseSchema):
    quiz: "QuizSchemaWithoutResource"

from .quiz_schema import QuizSchema, QuizSchemaWithoutResource
