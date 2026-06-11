from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QuizResultWithoutUserAndQuizSchema(BaseModel):
    quiz_result_id: UUID

    quiz_id: UUID

    user_id: str

    completed_at: datetime
    percent: int


class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: PlainUserSchema
    quiz: BaseQuizSchema


from application.schemas.quiz_schema import BaseQuizSchema  # noqa
from application.schemas.user_schema import PlainUserSchema  # noqa
