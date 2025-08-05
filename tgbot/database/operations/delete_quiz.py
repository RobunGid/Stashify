from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.quiz import QuizModel

async def delete_quiz(resource_id: UUID4) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(QuizModel).where(QuizModel.resource_id==resource_id)
        quiz = (await session.execute(statement)).scalars().first()
        if not quiz:
            raise ValueError("No such quiz")
        await session.delete(quiz)
        await session.commit()
        