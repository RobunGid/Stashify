from schemas.category_schema import CategorySchema
from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel

async def create_category(category_data: CategorySchema):
    async with AsyncSessionLocal() as session:
        category = CategoryModel(**category_data.model_dump())
        session.add(category)
        await session.commit()