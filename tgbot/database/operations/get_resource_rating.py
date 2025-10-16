from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.resource_rating_schema import ResourceRatingSchema
from database.models.resource_rating import ResourceRatingModel
from database.models.resource import ResourceModel
from database.models.user import UserModel
from database.orm import AsyncSessionLocal

async def get_resource_rating(resource_id: UUID4, user_id: str) -> ResourceRatingSchema | None:
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