from sqlalchemy import update
from database.orm import AsyncSessionLocal
from schemas.quiz_question_schema import QuizQuestionBaseSchema
from database.models.quiz_question import QuizQuestionModel

async def update_quiz_question(quiz_question_data: QuizQuestionBaseSchema):
    async with AsyncSessionLocal() as session:
        statement = update(QuizQuestionModel).where(QuizQuestionModel.id == quiz_question_data.id).values(**quiz_question_data.model_dump())
        await session.execute(statement)
        await session.commit()