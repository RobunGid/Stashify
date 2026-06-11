from uuid import UUID

from pydantic import ConfigDict, Field
from application.schemas.base_schema import BaseSchema


class BaseQuizItemSchema(BaseSchema):
    quiz_id: UUID = Field()
    resource_item_id: UUID

    model_config = ConfigDict(from_attributes=True)


class QuizSchema(BaseQuizItemSchema):
    resource: ResourceItemSchema
    questions: list[QuizQuestionBaseSchema] = Field(default_factory=list)


from application.schemas.quiz_question_schema import QuizQuestionBaseSchema  # noqa
from application.schemas.resource_schema import ResourceItemSchema  # noqa
