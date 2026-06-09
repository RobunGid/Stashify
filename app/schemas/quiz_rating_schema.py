from datetime import datetime

from pydantic import BaseModel


class QuizRatingSchema(BaseModel):
    id: str

    quiz_id: str
    quiz: "QuizSchema"

    user_id: str
    user: "UserSchema"

    created_at: datetime
    rating: int


from .quiz_schema import QuizSchema
from .user_schema import UserSchema
