from typing import List

from pydantic import BaseModel, ConfigDict, Field, UUID4

from schemas.quiz_question_schema import QuizQuestionBaseSchema
from schemas.resource_schema import ResourceSchema


class PlainQuizSchema(BaseModel):
    quiz_id: UUID4 = Field()

    resource_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class QuizSchemaWithoutResource(PlainQuizSchema):
    questions: List[QuizQuestionBaseSchema] = Field(default_factory=list)


class QuizSchema(QuizSchemaWithoutResource):
    resource: ResourceSchema
