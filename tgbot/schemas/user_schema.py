from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from database.models.user import Role

class UserSchema(BaseModel):
    id: str
    tg_id: str = Field()
    
    role: Role
    language: str
    
    connection_date: datetime = Field(default_factory=datetime.now)
    
    quiz_results: "List[QuizResultSchema]" = Field(default_factory=list)
    quiz_ratings: "List[QuizRatingSchema]" = Field(default_factory=list)
    
from .quiz_result_schema import QuizResultSchema
from .quiz_rating_schema import QuizRatingSchema