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


class QuizQuestionSchema(BaseQuizQuestionSchema):
    quiz: BaseQuizItemSchema


from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
