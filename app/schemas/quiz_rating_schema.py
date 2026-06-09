from datetime import datetime

from pydantic import BaseModel

from schemas.quiz_schema import QuizSchema


class QuizRatingWithoutUserSchema(BaseModel):
    quiz_rating_id: str

    quiz_id: str
    quiz: QuizSchema

    user_id: str

    created_at: datetime
    rating: int


class QuizRatingSchema(BaseModel):
    user: UserSchema


from schemas.user_schema import UserSchema  # noqa
