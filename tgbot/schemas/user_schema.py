from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from database.models.user import Role

class UserSchema(BaseModel):
    id: str
    tg_id: str = Field(exclude=True)
    
    role: Role
    connection_date: datetime
    
    quiz_results: "List[QuizResultSchema]"
    quiz_ratings: "List[QuizRatingSchema]"
    
from quiz_result_schema import QuizResultSchema
from quiz_rating_schema import QuizRatingSchema