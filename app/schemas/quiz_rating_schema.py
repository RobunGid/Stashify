from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from schemas.quiz_schema import QuizSchema

if TYPE_CHECKING:
    from schemas.user_schema import UserSchema


class QuizRatingSchema(BaseModel):
    quiz_rating_id: str

    quiz_id: str
    quiz: QuizSchema

    user_id: str
    user: UserSchema

    created_at: datetime
    rating: int
