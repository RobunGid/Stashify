from datetime import datetime

from pydantic import BaseModel

from schemas.quiz_schema import QuizSchema
from schemas.user_schema import UserSchema


class QuizRatingSchema(BaseModel):
    quiz_rating_id: str

    quiz_id: str
    quiz: QuizSchema

    user_id: str
    user: UserSchema

    created_at: datetime
    rating: int
