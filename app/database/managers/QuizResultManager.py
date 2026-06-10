from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models.quiz import QuizModel
from database.models.quiz_result import QuizResultModel
from database.orm import AsyncSessionLocal
from schemas.quiz_result_schema import QuizResultSchema, QuizResultWithoutUserAndQuizSchema


class QuizResultManager:
    @classmethod
    async def create(cls, quiz_result_data: QuizResultWithoutUserAndQuizSchema):
        async with AsyncSessionLocal() as session:
            quiz_result = QuizResultModel(
                id=uuid4(),
                quiz_id=quiz_result_data.quiz_id,
                user_id=quiz_result_data.user_id,
                completed_at=quiz_result_data.completed_at,
                percent=quiz_result_data.percent,
            )
            session.add(quiz_result)
            await session.commit()

    @classmethod
    async def get_one(cls, resource_item_id: UUID, user_id: str):
        async with AsyncSessionLocal() as session:
            statement = (
                select(QuizResultModel)
                .options(
                    selectinload(QuizResultModel.quiz),
                )
                .options(
                    selectinload(QuizResultModel.user),
                )
                .options(
                    selectinload(QuizResultModel.quiz).selectinload(QuizModel.resource),
                )
            )

            statement = statement.filter(QuizResultModel.user_id == user_id).filter(
                QuizModel.resource_item_id == resource_item_id,
            )
            quiz_result = (await session.execute(statement)).scalars().first()
            if quiz_result:
                return QuizResultSchema.model_validate(
                    quiz_result,
                    from_attributes=True,
                )
            else:
                return None

    @classmethod
    async def delete(cls, resource_item_id: UUID, user_id: str) -> None:
        async with AsyncSessionLocal() as session:
            statement = (
                select(QuizResultModel)
                .filter(QuizResultModel.user_id == user_id)
                .filter(QuizModel.resource_item_id == resource_item_id)
            )
            quiz_result = (await session.execute(statement)).scalars().first()
            if not quiz_result:
                raise ValueError("No such quiz result")
            await session.delete(quiz_result)
            await session.commit()
