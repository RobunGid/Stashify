from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from database.models.user import Role

class PlainUserSchema(BaseModel):
    id: str = Field()
    username: Optional[str]
    
    role: Role
    language: str
    
    connection_date: datetime = Field(default_factory=datetime.now)
    
class UserSchema(PlainUserSchema):
    quiz_results: "List[QuizResultWithoutUserAndQuizSchema]" = Field(default_factory=list)
    quiz_ratings: "List[QuizRatingSchema]" = Field(default_factory=list)
    
from .quiz_result_schema import QuizResultWithoutUserAndQuizSchema
from .quiz_rating_schema import QuizRatingSchema