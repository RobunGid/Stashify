from typing import overload

from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.resource_rating import ResourceRatingModel

@overload
async def delete_resource_rating(user_id: None, resource_id: None, resource_rating_id: UUID4) -> None: ...

@overload
async def delete_resource_rating(user_id: str, resource_id: UUID4, resource_rating_id: None = None) -> None: ...

async def delete_resource_rating(user_id = None, resource_id = None, resource_rating_id = None):
    async with AsyncSessionLocal() as session:
        if resource_rating_id:
            statement = select(ResourceRatingModel).where(ResourceRatingModel.id == resource_rating_id)
            favorite = (await session.execute(statement)).scalars().first()
            await session.delete(favorite)
            await session.commit()
        if user_id and resource_id:
            statement = select(ResourceRatingModel).where(ResourceRatingModel.user_id == user_id).where(ResourceRatingModel.resource_id == resource_id)
            favorite = (await session.execute(statement)).scalars().first()
            await session.delete(favorite)
            await session.commit()