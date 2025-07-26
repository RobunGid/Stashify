
from typing import List

from pydantic import BaseModel

class QuizQuestionSchema(BaseModel):
    id: str
    
    quiz_id: str
    quiz: "QuizSchema"
    
    options: List[str]
    answer: str
    
from quiz_schema import QuizSchema
