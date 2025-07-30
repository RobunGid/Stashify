from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel

async def delete_category(id: UUID4) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(CategoryModel).where(CategoryModel.id==id)
        category = (await session.execute(statement)).scalars().first()
        if not category:
            raise ValueError("No such category")
        await session.delete(category)
        await session.commit()
        