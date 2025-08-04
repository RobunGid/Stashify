from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from schemas.category_schema import CategorySchema

async def get_categories() -> List[CategorySchema]:
    async with AsyncSessionLocal() as session:
        statement = select(CategoryModel)\
        .options(
            selectinload(CategoryModel.resources).selectinload(ResourceModel.quizes).selectinload(QuizModel.questions)
		)
        categories = (await session.execute(statement)).scalars().all()
        
        return [CategorySchema.model_validate(category, from_attributes=True) for category in categories]