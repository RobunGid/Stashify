from pydantic import BaseModel, ConfigDict, UUID4


class QuizQuestionBaseSchema(BaseModel):
    quiz_question_id: UUID4
    text: str

    quiz_id: UUID4

    options: list[str]
    right_options: list[int]

    image: str | None
    model_config = ConfigDict(from_attributes=True)


class QuizQuestionSchema(QuizQuestionBaseSchema):
    quiz: QuizSchema


class QuizQuestionWithoutResourceSchema(QuizQuestionBaseSchema):
    quiz: PlainQuizSchema


from schemas.quiz_schema import PlainQuizSchema, QuizSchema
