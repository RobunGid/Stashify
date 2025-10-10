from typing import List, Optional, overload
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.favorite import FavoriteModel
from database.models.user import UserModel
from database.models.resource import ResourceModel
from schemas.favorite_schema import FavoriteSchema

@overload
async def get_user_favorites(user_id: UUID4, tg_user_id: None): ...

@overload
async def get_user_favorites(user_id: None, tg_user_id: str): ...

async def get_user_favorites(user_id, tg_user_id) -> List[FavoriteSchema]:
    async with AsyncSessionLocal() as session:
        statement = select(FavoriteModel)\
        .options(
            selectinload(FavoriteModel.user).\
                selectinload(UserModel.quiz_results)
        )\
        .options(
            selectinload(FavoriteModel.user).\
                selectinload(UserModel.quiz_ratings)
        )\
        .options(
            selectinload(FavoriteModel.resource).\
                selectinload(ResourceModel.category)
        )\
        .options(
            selectinload(FavoriteModel.resource).\
                selectinload(ResourceModel.quiz)
        )
        if user_id:
            statement = statement.where(FavoriteModel.user_id==user_id)
        if tg_user_id:
            statement = statement.join(FavoriteModel.user).where(UserModel.tg_id==tg_user_id)
        
        favorites = (await session.execute(statement)).scalars().all()
        
        return [FavoriteSchema.model_validate(favorite, from_attributes=True) for favorite in favorites]