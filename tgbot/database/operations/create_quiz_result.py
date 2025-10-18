from schemas.quiz_result_schema import QuizResultSchema
from database.orm import AsyncSessionLocal
from database.models.quiz_result import QuizResultModel


async def create_quiz_result(quiz_result_data: QuizResultSchema):
    async with AsyncSessionLocal() as session:
        quiz_result = QuizResultModel(**quiz_result_data.model_dump(exclude=("quiz", "user_id")), user_id=quiz_result_data.user_id)
        session.add(quiz_result)
        await session.commit()