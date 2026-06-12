from typing import List, Optional
from uuid import UUID, uuid4

from application.schemas.base_schema import BaseSchema
from domain.entities.user_account import UserAccountEntity
from infrastructure.models.user_account import Role
from pydantic import Field


class BaseUserAccountSchema(BaseSchema):
    user_account_id: UUID = Field(default_factory=uuid4)
    user_telegram_id: int
    username: Optional[str]

    role: Role = Field(default=Role.user)

    def to_entity(self) -> UserAccountEntity:
        return UserAccountEntity(
            user_account_id=self.user_account_id,
            user_telegram_id=self.user_telegram_id,
            username=self.username,
            role=self.role,
        )


class UserAccountSchema(BaseUserAccountSchema):
    quiz_results: List[BaseQuizResultSchema] = Field(
        default_factory=list,
    )
    quiz_ratings: List[BaseQuizRatingSchema] = Field(default_factory=list)


from application.schemas.quiz_rating_schema import BaseQuizRatingSchema  # noqa
from application.schemas.quiz_result_schema import BaseQuizResultSchema  # noqa
