from datetime import datetime
from uuid import UUID

from application.schemas.quiz_schema import QuizSchema
from pydantic import BaseModel


class QuizRatingWithoutUserSchema(BaseModel):
    quiz_rating_id: str

    quiz_id: UUID
    quiz: QuizSchema

    user_id: str

    created_at: datetime
    rating: int


class QuizRatingSchema(BaseModel):
    user: UserSchema


from application.schemas.user_schema import UserSchema  # noqa
