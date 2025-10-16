from database.orm import AsyncSessionLocal
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from database.models.resource_rating import ResourceRatingModel

async def create_resource_rating(resource_rating_data: ResourceRatingWithoutUserAndResourceSchema):
    async with AsyncSessionLocal() as session:
        resource_rating = ResourceRatingModel(**resource_rating_data.model_dump())
        session.add(resource_rating)
        await session.commit()