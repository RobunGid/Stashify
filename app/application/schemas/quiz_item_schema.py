from uuid import UUID

from application.schemas.base_schema import BaseSchema
from domain.entities.quiz_item import QuizItemEntity
from pydantic import ConfigDict, Field


class BaseQuizItemSchema(BaseSchema[QuizItemEntity]):
    quiz_item_id: UUID
    resource_item_id: UUID

    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> QuizItemEntity:
        return QuizItemEntity(
            quiz_item_id=self.quiz_item_id,
            resource_item_id=self.resource_item_id,
        )


class QuizItemSchema(BaseQuizItemSchema):
    resource_item: ResourceItemSchema
    quiz_questions: list[BaseQuizQuestionSchema] = Field(default_factory=list)


from application.schemas.quiz_question_schema import BaseQuizQuestionSchema  # noqa
from application.schemas.resource_item_schema import ResourceItemSchema  # noqa
