from database.orm import AsyncSessionLocal
from schemas.quiz_question_schema import QuizQuestionBaseSchema
from database.models.quiz_question import QuizQuestionModel

async def create_quiz_question(quiz_question_data: QuizQuestionBaseSchema):
    async with AsyncSessionLocal() as session:
        quiz_question = QuizQuestionModel(**quiz_question_data.model_dump())
        session.add(quiz_question)
        await session.commit()