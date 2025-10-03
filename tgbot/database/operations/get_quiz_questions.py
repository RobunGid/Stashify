from typing import List, Optional
from sqlalchemy import select, column
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from schemas.quiz_question_schema import QuizQuestionWithoutResourceSchema
from database.models.quiz_question import QuizQuestionModel

async def get_quiz_questions(resource_id: UUID4) -> List[QuizQuestionWithoutResourceSchema]:
    async with AsyncSessionLocal() as session:
        statement = select(QuizQuestionModel)\
        .options(
            selectinload(QuizQuestionModel.quiz)
        )
        statement = statement.filter(QuizModel.resource_id == resource_id)
        quiz_questions = (await session.execute(statement)).scalars().all()
        
        return [QuizQuestionWithoutResourceSchema.model_validate(quiz_question, from_attributes=True) for quiz_question in quiz_questions]