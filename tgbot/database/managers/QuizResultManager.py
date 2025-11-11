from uuid import uuid4

from schemas.quiz_result_schema import QuizResultSchema
from database.orm import AsyncSessionLocal
from database.models.quiz_result import QuizResultModel

class QuizResultManager:
    @classmethod
    async def create_quiz_result(cls, quiz_result_data: QuizResultSchema):
        async with AsyncSessionLocal() as session:
            quiz_result = QuizResultModel(
                id=uuid4(),
                quiz_id=quiz_result_data.quiz_id,
                user_id=quiz_result_data.user_id,
                completed_at=quiz_result_data.completed_at,
                percent=quiz_result_data.percent
            )
            session.add(quiz_result)
            await session.commit()