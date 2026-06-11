from datetime import datetime
from uuid import UUID

from application.schemas.quiz_item_schema import QuizSchema
from pydantic import BaseModel

from application.schemas.base_schema import BaseSchema


class QuizRatingWithoutUserSchema(BaseModel):
    quiz_rating_id: str

    quiz_id: UUID
    quiz: QuizSchema

    user_id: str

    created_at: datetime
    rating: int


class QuizRatingSchema(BaseModel):
    user: UserAccountSchema


from application.schemas.user_account_schema import UserAccountSchema  # noqa
