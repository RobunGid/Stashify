from uuid import UUID

from application.schemas.base_schema import BaseSchema, BaseUpdateSchema
from application.schemas.quiz_question_schema import BaseQuizQuestionSchema
from domain.entities.quiz_option import QuizOptionEntity, QuizOptionUpdateEntity
from pydantic import ConfigDict


class BaseQuizOptionSchema(BaseSchema[QuizOptionEntity]):
    quiz_question_id: UUID

    text: str
    is_right: bool

    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> QuizOptionEntity:
        return QuizOptionEntity(quiz_question_id=self.quiz_question_id, text=self.text, is_right=self.is_right)


class QuizOptionUpdateSchema(BaseUpdateSchema[QuizOptionUpdateEntity]):
    text: str | None
    is_right: bool | None

    def to_entity(self) -> QuizOptionUpdateEntity:
        return QuizOptionUpdateEntity(text=self.text, is_right=self.is_right)


class QuizOptionSchema(BaseQuizOptionSchema):
    quiz_question: BaseQuizQuestionSchema
