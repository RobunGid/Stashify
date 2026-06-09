from pydantic import BaseModel, ConfigDict, Field, UUID4


class PlainQuizSchema(BaseModel):
    quiz_id: UUID4 = Field()

    resource_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class QuizSchemaWithoutResource(PlainQuizSchema):
    questions: list[QuizQuestionBaseSchema] = Field(default_factory=list)


class QuizSchema(QuizSchemaWithoutResource):
    resource: ResourceSchema


from schemas.quiz_question_schema import QuizQuestionBaseSchema  # noqa
from schemas.resource_schema import ResourceSchema  # noqa
