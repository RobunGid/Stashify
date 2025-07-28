from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel
from schemas.category_schema import CategorySchema

async def get_categories() -> List[CategorySchema]:
    async with AsyncSessionLocal() as session:
        statement = select(CategoryModel).options(selectinload(CategoryModel.resources))
        categories = (await session.execute(statement)).scalars().all()
        
        return [CategorySchema.model_validate(category) for category in categories]