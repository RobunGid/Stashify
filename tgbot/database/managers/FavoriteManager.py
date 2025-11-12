from typing import List, overload

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from schemas.favorite_schema import FavoriteSchema
from database.orm import AsyncSessionLocal
from database.models.user import UserModel
from database.models.resource import ResourceModel
from database.models.favorite import FavoriteModel

class FavoriteManager:
    @classmethod
    async def create(cls, favorite_data: FavoriteSchema):
        async with AsyncSessionLocal() as session:
            favorite = FavoriteModel(
                id=favorite_data.id,
                user_id=favorite_data.user_id,
                resource_id=favorite_data.resource_id,
                added_at=favorite_data.added_at
            )
            session.add(favorite)
            await session.commit()
    @classmethod
    async def get_many(cls, user_id: str) -> List[FavoriteSchema]:
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
            statement = statement.where(FavoriteModel.user_id==user_id)

            favorites = (await session.execute(statement)).scalars().all()
            
            return [FavoriteSchema.model_validate(favorite, from_attributes=True) for favorite in favorites]
    
    @overload
    @classmethod
    async def delete(cls, user_id: None, resource_id: None, favorite_id: UUID4) -> None: ...

    @overload
    @classmethod
    async def delete(cls, user_id: str, resource_id: UUID4, favorite_id: None = None) -> None: ...

    @classmethod
    async def delete(cls, user_id = None, resource_id = None, favorite_id = None):
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