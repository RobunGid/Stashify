from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field

class QuizResultSchema(BaseModel):
    id: UUID4
    
    quiz_id: UUID4
    quiz: Optional["QuizSchema"] = Field(default_factory=lambda: None)
    
    user_id: str
    user: Optional["UserSchema"] = Field(default_factory=lambda: None)
    
    completed_at: datetime = Field(default_factory=datetime.now)
    percent: int
    
from .user_schema import UserSchema
from .quiz_schema import QuizSchema