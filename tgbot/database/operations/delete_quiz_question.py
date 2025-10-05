from typing import overload

from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.quiz_question import QuizQuestionModel
from database.models.quiz import QuizModel

@overload
async def delete_quiz_question(resource_id: UUID4, quiz_question_number: int, quiz_question_id: None) -> None: ...

@overload
async def delete_quiz_question(resource_id: UUID4, quiz_question_number: None, quiz_question_id: int) -> None: ...

async def delete_quiz_question(resource_id, quiz_question_number = None, quiz_question_id = None) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(QuizQuestionModel)\
            .join(QuizModel, QuizModel.id == QuizQuestionModel.quiz_id)\
            .where(QuizModel.resource_id == resource_id)
        if quiz_question_number != None:
            quiz_questions = (await session.execute(statement)).scalars().all()
            await session.delete(quiz_questions[quiz_question_number])
        if quiz_question_id != None:
            statement = statement.where(QuizQuestionModel.id == quiz_question_id)
            quiz_question = (await session.execute(statement)).scalars().first()
            await session.delete(quiz_question)
        await session.commit()