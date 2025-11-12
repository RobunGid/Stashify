from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


    
class QuizResultWithoutUserAndQuizSchema(BaseModel):
    id: UUID4
    
    quiz_id: UUID4
    
    user_id: str
    
    completed_at: datetime = Field(default_factory=datetime.now)
    percent: int
    
class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: Optional["UserSchema"] = Field(default_factory=lambda: None)
    quiz: Optional["QuizSchema"] = Field(default_factory=lambda: None)
    
from .user_schema import UserSchema
from .quiz_schema import QuizSchema