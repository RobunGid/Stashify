from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.schemas.base_schema import BaseSchema


class QuizResultWithoutUserAndQuizSchema(BaseModel):
    quiz_result_id: UUID

    quiz_id: UUID

    user_id: str

    completed_at: datetime
    percent: int


class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: PlainUserAccountSchema
    quiz: BaseQuizItemSchema


from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
from application.schemas.user_account_schema import PlainUserAccountSchema  # noqa
