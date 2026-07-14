from uuid import UUID

from application.schemas.base_schema import BaseSchema, BaseUpdateSchema
from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from pydantic import ConfigDict


class BaseQuizQuestionSchema(BaseSchema[QuizQuestionEntity]):
    quiz_question_id: UUID
    text: str

    quiz_item_id: UUID

    image: str | None
    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> QuizQuestionEntity:
        return QuizQuestionEntity(
            quiz_question_id=self.quiz_question_id,
            text=self.text,
            quiz_item_id=self.quiz_item_id,
            image=self.image,
        )


class QuizQuestionUpdateSchema(BaseUpdateSchema[QuizQuestionUpdateEntity]):
    text: str | None

    options: list[str] | None
    right_options: list[int] | None

    image: str | None

    def to_entity(self) -> QuizQuestionUpdateEntity:
        return QuizQuestionUpdateEntity(
            text=self.text,
            image=self.image,
        )


class QuizQuestionSchema(BaseQuizQuestionSchema):
    quiz: BaseQuizItemSchema


from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
