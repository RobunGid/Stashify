from datetime import datetime
from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.quiz_result import QuizResultEntity


class BaseQuizResultSchema(BaseSchema[QuizResultEntity]):
    quiz_result_id: UUID

    quiz_item_id: UUID

    user_account_id: str

    completed_at: datetime
    percent: int

    def to_entity(self) -> QuizResultEntity:
        return QuizResultEntity(
            quiz_result_id=self.quiz_result_id,
            quiz_item_id=self.quiz_item_id,
            user_account_id=self.user_account_id,
            percent=self.percent,
        )


class QuizResultSchema(BaseQuizResultSchema):
    user: BaseUserAccountSchema
    quiz: BaseQuizItemSchema


from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
from application.schemas.user_account_schema import BaseUserAccountSchema  # noqa
