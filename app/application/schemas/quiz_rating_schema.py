from uuid import UUID

from application.schemas.base_schema import BaseSchema
from application.schemas.quiz_item_schema import QuizSchema


class BaseQuizRatingSchema(BaseSchema):
    quiz_rating_id: str

    quiz_item_id: UUID

    user_account_id: str

    rating: int


class QuizRatingSchema(BaseQuizRatingSchema):
    user: UserAccountSchema
    quiz: QuizSchema


from application.schemas.user_account_schema import UserAccountSchema  # noqa
