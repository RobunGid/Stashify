from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, UUID4

from schemas.quiz_schema import PlainQuizSchema

if TYPE_CHECKING:
    from schemas.user_schema import PlainUserSchema


class QuizResultWithoutUserAndQuizSchema(BaseModel):
    quiz_result_id: UUID4

    quiz_id: UUID4

    user_id: str

    completed_at: datetime = Field(default_factory=datetime.now)
    percent: int


class QuizResultSchema(QuizResultWithoutUserAndQuizSchema):
    user: PlainUserSchema | None = Field(default_factory=lambda: None)
    quiz: PlainQuizSchema | None = Field(default_factory=lambda: None)
