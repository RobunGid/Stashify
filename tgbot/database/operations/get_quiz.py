from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.quiz import QuizModel
from schemas.quiz_schema import QuizSchema

async def get_quiz(resource_id: UUID4) -> QuizSchema:
    async with AsyncSessionLocal() as session:
        statement = select(QuizModel)\
        .options(
            selectinload(QuizModel.questions)
        )\
        .options(
            selectinload(QuizModel.resource)
        )
        statement = statement.filter(QuizModel.resource_id == resource_id)
        quiz = (await session.execute(statement)).scalars().first()
        
        return QuizSchema.model_validate(quiz, from_attributes=True)