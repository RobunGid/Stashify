from typing import overload, List

from pydantic import UUID4
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from schemas.quiz_question_schema import QuizQuestionBaseSchema, QuizQuestionWithoutResourceSchema
from database.orm import AsyncSessionLocal
from database.models.quiz_question import QuizQuestionModel
from database.models.quiz import QuizModel

class QuizQuestionManager:
    @classmethod
    async def create(cls, quiz_question_data: QuizQuestionBaseSchema):
        async with AsyncSessionLocal() as session:
            quiz_question = QuizQuestionModel(**quiz_question_data.model_dump())
            session.add(quiz_question)
            await session.commit()
            
    @overload
    @classmethod
    async def delete(cls, resource_id: str, quiz_question_number: int, quiz_question_id: None) -> None: ...
    
    @overload
    @classmethod
    async def delete(cls, resource_id: UUID4, quiz_question_number: int, quiz_question_id: None) -> None: ...

    @overload
    @classmethod
    async def delete(cls, resource_id: str, quiz_question_number: None, quiz_question_id: int) -> None: ...
    
    @overload
    @classmethod
    async def delete(cls, resource_id: UUID4, quiz_question_number: None, quiz_question_id: int) -> None: ...

    @classmethod
    async def delete(cls, resource_id, quiz_question_number = None, quiz_question_id = None) -> None:
        async with AsyncSessionLocal() as session:
            statement = select(QuizQuestionModel)\
                .join(QuizModel, QuizModel.id == QuizQuestionModel.quiz_id)\
                .where(QuizModel.resource_id == resource_id)
            if quiz_question_number is not None:
                quiz_questions = (await session.execute(statement)).scalars().all()
                await session.delete(quiz_questions[quiz_question_number])
            if quiz_question_id is not None:
                statement = statement.where(QuizQuestionModel.id == quiz_question_id)
                quiz_question = (await session.execute(statement)).scalars().first()
                await session.delete(quiz_question)
            await session.commit()

    @classmethod
    async def get_many(cls, resource_id: UUID4) -> List[QuizQuestionWithoutResourceSchema]:
        async with AsyncSessionLocal() as session:
            statement = select(QuizQuestionModel)\
            .options(
                selectinload(QuizQuestionModel.quiz)
            )
            statement = statement.filter(QuizModel.resource_id == resource_id)
            quiz_questions = (await session.execute(statement)).scalars().all()
            
            return [QuizQuestionWithoutResourceSchema.model_validate(quiz_question, from_attributes=True) for quiz_question in quiz_questions]
        
    @classmethod
    async def update(cls, quiz_question_data: QuizQuestionBaseSchema):
        async with AsyncSessionLocal() as session:
            statement = update(QuizQuestionModel).where(QuizQuestionModel.id == quiz_question_data.id).values(**quiz_question_data.model_dump())
            await session.execute(statement)
            await session.commit()