from typing import overload

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema, ResourceRatingSchema
from database.models.resource_rating import ResourceRatingModel
from database.models.resource import ResourceModel
from database.models.user import UserModel

class ResourceRatingManager:
    @classmethod
    async def create_resource_rating(cls, resource_rating_data: ResourceRatingWithoutUserAndResourceSchema):
        async with AsyncSessionLocal() as session:
            resource_rating = ResourceRatingModel(**resource_rating_data.model_dump())
            session.add(resource_rating)
            await session.commit()
            
    @overload
    @classmethod
    async def delete_resource_rating(cls, user_id: None, resource_id: None, resource_rating_id: UUID4): ...

    @overload
    @classmethod
    async def delete_resource_rating(cls, user_id: str, resource_id: UUID4, resource_rating_id: None = None): ...

    @classmethod
    async def delete_resource_rating(cls, user_id = None, resource_id = None, resource_rating_id = None):
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
                
    @classmethod
    async def get_resource_rating(cls, resource_id: UUID4, user_id: str) -> ResourceRatingSchema | None:
        async with AsyncSessionLocal() as session:
            statement = select(ResourceRatingModel)
            statement = statement\
            .filter(ResourceRatingModel.resource_id == resource_id)\
            .filter(ResourceRatingModel.user_id == user_id)\
            .options(
                selectinload(ResourceRatingModel.resource).selectinload(ResourceModel.quiz)
            )\
            .options(
                selectinload(ResourceRatingModel.resource).selectinload(ResourceModel.category)
            )\
            .options(
                selectinload(ResourceRatingModel.user).selectinload(UserModel.quiz_results)
            )\
            .options(
                selectinload(ResourceRatingModel.user).selectinload(UserModel.quiz_ratings)
            )
            resource_rating = (await session.execute(statement)).scalars().first()
            
            if resource_rating is None:
                return None    
            return ResourceRatingSchema.model_validate(resource_rating, from_attributes=True) 