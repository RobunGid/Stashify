from typing import overload

from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.favorite import FavoriteModel
from schemas.favorite_schema import FavoriteSchema

@overload
async def remove_favorite(user_id: None, resource_id: None, favorite_id: UUID4) -> None: ...

@overload
async def remove_favorite(user_id: str, resource_id: UUID4, favorite_id: None = None) -> None: ...

async def remove_favorite(user_id = None, resource_id = None, favorite_id = None):
    async with AsyncSessionLocal() as session:
        if favorite_id:
            statement = select(FavoriteModel).where(FavoriteModel.id == favorite_id)
            favorite = (await session.execute(statement)).scalars().first()
            await session.delete(favorite)
            await session.commit()
        if user_id and resource_id:
            statement = select(FavoriteModel).where(FavoriteModel.user_id == user_id).where(FavoriteModel.resource_id == resource_id)
            favorite = (await session.execute(statement)).scalars().first()
            await session.delete(favorite)
            await session.commit()