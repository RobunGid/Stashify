from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, UUID4

from schemas.quiz_question_schema import QuizQuestionBaseSchema

if TYPE_CHECKING:
    from schemas.resource_schema import ResourceSchema


class PlainQuizSchema(BaseModel):
    quiz_id: UUID4 = Field()

    resource_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class QuizSchemaWithoutResource(PlainQuizSchema):
    questions: list[QuizQuestionBaseSchema] = Field(default_factory=list)


class QuizSchema(QuizSchemaWithoutResource):
    resource: ResourceSchema
