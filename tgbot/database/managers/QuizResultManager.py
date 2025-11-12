from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.quiz_result_schema import QuizResultSchema
from database.orm import AsyncSessionLocal
from database.models.quiz_result import QuizResultModel
from database.models.quiz import QuizModel

class QuizResultManager:
    @classmethod
    async def create(cls, quiz_result_data: QuizResultSchema):
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
            
    @classmethod
    async def get_one(cls, resource_id: UUID4):
        async with AsyncSessionLocal() as session:
            statement = select(QuizResultModel)\
                .options(
                    selectinload(QuizResultModel.quiz)
                )

            statement = statement.filter(QuizResultModel.quiz.resource_id == resource_id)
            quiz = (await session.execute(statement)).scalars().first()
                
            return QuizResultSchema.model_validate(quiz, from_attributes=True)
        
    @classmethod
    async def delete(cls, resource_id: UUID4, user_id: str) -> None:
        async with AsyncSessionLocal() as session:
            statement = select(QuizResultModel)\
                .filter(QuizResultModel.user_id==user_id)\
                .filter(QuizModel.resource_id==resource_id)
            quiz = (await session.execute(statement)).scalars().first()
            if not quiz:
                raise ValueError("No such quiz result")
            await session.delete(quiz)
            await session.commit()