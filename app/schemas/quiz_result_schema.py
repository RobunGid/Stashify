from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class QuizResultWithoutUserAndQuizSchema(BaseModel):
    quiz_result_id: UUID

    quiz_id: UUID

    user_id: str

    completed_at: datetime = Field(default_factory=datetime.now)
    percent: int


class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: PlainUserSchema
    quiz: PlainQuizSchema


from schemas.quiz_schema import PlainQuizSchema  # noqa
from schemas.user_schema import PlainUserSchema  # noqa
