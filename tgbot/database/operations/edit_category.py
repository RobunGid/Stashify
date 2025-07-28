from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel

async def edit_category(id: UUID4, new_name: str) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(CategoryModel).where(CategoryModel.id==id)
        category = (await session.execute(statement)).scalars().first()
        if not category:
            raise ValueError("No such category")
        category.name = new_name # type: ignore
        await session.commit()
        