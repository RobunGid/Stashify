from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4


class QuizResultWithoutUserAndQuizSchema(BaseModel):
    id: UUID4

    quiz_id: UUID4

    user_id: str

    completed_at: datetime = Field(default_factory=datetime.now)
    percent: int


class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: Optional["PlainUserSchema"] = Field(default_factory=lambda: None)
    quiz: Optional["PlainQuizSchema"] = Field(default_factory=lambda: None)


from .quiz_schema import PlainQuizSchema
from .user_schema import PlainUserSchema
