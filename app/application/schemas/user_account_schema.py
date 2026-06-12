from typing import List, Optional
from uuid import UUID, uuid4

from application.schemas.base_schema import BaseSchema
from domain.entities.user_account import UserAccountEntity
from infrastructure.models.user_account import Role
from pydantic import Field


class PlainUserAccountSchema(BaseSchema):
    user_account_id: UUID = Field(default_factory=uuid4)
    telegram_id: int
    username: Optional[str]

    role: Role = Field(default=Role.user)


class UserAccountSchema(PlainUserAccountSchema):
    quiz_results: List[QuizResultWithoutUserAndQuizSchema] = Field(
        default_factory=list,
    )
    quiz_ratings: List[QuizRatingWithoutUserSchema] = Field(default_factory=list)

    def to_entity(self) -> UserAccountEntity:
        return UserAccountEntity(**self.model_dump())


from application.schemas.quiz_rating_schema import QuizRatingWithoutUserSchema  # noqa
from application.schemas.quiz_result_schema import QuizResultWithoutUserAndQuizSchema  # noqa
