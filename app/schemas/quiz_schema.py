from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseQuizSchema(BaseModel):
    quiz_id: UUID = Field()
    resource_item_id: UUID

    model_config = ConfigDict(from_attributes=True)


class QuizSchema(BaseQuizSchema):
    resource: ResourceItemSchema
    questions: list[QuizQuestionBaseSchema] = Field(default_factory=list)


from schemas.quiz_question_schema import QuizQuestionBaseSchema  # noqa
from schemas.resource_schema import ResourceItemSchema  # noqa
