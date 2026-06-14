from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.quiz_question import QuizQuestionEntity
from pydantic import ConfigDict


class BaseQuizQuestionSchema(BaseSchema[QuizQuestionEntity]):
    quiz_question_id: UUID
    text: str

    quiz_item_id: UUID

    options: list[str]
    right_options: list[int]

    image: str | None
    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> QuizQuestionEntity:
        return QuizQuestionEntity(
            quiz_question_id=self.quiz_question_id,
            text=self.text,
            quiz_item_id=self.quiz_item_id, 
            options=self.options,
            right_options=self.right_options,
            image=self.image,
        )


class QuizQuestionSchema(BaseQuizQuestionSchema):
    quiz: BaseQuizItemSchema


from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
