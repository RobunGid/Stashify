from datetime import datetime
from typing import List, Optional

from infrastructure.models.user import Role
from pydantic import BaseModel, Field


class PlainUserSchema(BaseModel):
    user_id: str
    username: Optional[str]

    role: Role

    connection_date: datetime


class UserSchema(PlainUserSchema):
    quiz_results: List[QuizResultWithoutUserAndQuizSchema] = Field(
        default_factory=list,
    )
    quiz_ratings: List[QuizRatingWithoutUserSchema] = Field(default_factory=list)


from application.schemas.quiz_rating_schema import QuizRatingWithoutUserSchema  # noqa
from application.schemas.quiz_result_schema import QuizResultWithoutUserAndQuizSchema  # noqa
