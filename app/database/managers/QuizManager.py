from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models.quiz import QuizModel
from database.models.quiz_question import QuizQuestionModel
from database.orm import AsyncSessionLocal
from schemas.quiz_schema import QuizSchema


class QuizManager:
    @classmethod
    async def create(cls, quiz_data: QuizSchema):
        async with AsyncSessionLocal() as session:
            quiz = QuizModel(**quiz_data.model_dump(exclude={"questions", "resource"}))
            quiz_questions = [
                QuizQuestionModel(**quiz_question_data.model_dump(exclude={"quiz"}))
                for quiz_question_data in quiz_data.questions
            ]
            session.add(quiz)
            session.add_all(quiz_questions)
            await session.commit()

    @classmethod
    async def delete(cls, resource_item_id: UUID) -> None:
        async with AsyncSessionLocal() as session:
            statement = select(QuizModel).where(QuizModel.resource_item_id == resource_item_id)
            quiz = (await session.execute(statement)).scalars().first()
            if not quiz:
                raise ValueError("No such quiz")
            await session.delete(quiz)
            await session.commit()

    @classmethod
    async def get_one(cls, resource_item_id: UUID) -> QuizSchema:
        async with AsyncSessionLocal() as session:
            statement = (
                select(QuizModel)
                .options(
                    selectinload(QuizModel.questions),
                )
                .options(
                    selectinload(QuizModel.resource_item),
                )
            )
            statement = statement.filter(QuizModel.resource_item_id == resource_item_id)
            quiz = (await session.execute(statement)).scalars().first()

            return QuizSchema.model_validate(quiz, from_attributes=True)
