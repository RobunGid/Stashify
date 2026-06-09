from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from database.models.user import Role


class PlainUserSchema(BaseModel):
    user_id: str = Field()
    username: Optional[str]

    role: Role
    language: str

    connection_date: datetime = Field(default_factory=datetime.now)


class UserSchema(PlainUserSchema):
    quiz_results: List[QuizResultWithoutUserAndQuizSchema] = Field(
        default_factory=list,
    )
    quiz_ratings: List[QuizRatingWithoutUserSchema] = Field(default_factory=list)


from schemas.quiz_rating_schema import QuizRatingWithoutUserSchema  # noqa
from schemas.quiz_result_schema import QuizResultWithoutUserAndQuizSchema  # noqa
