from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from schemas.resource_schema import ResourceSchema

async def create_resource(resource_data: ResourceSchema):
    async with AsyncSessionLocal() as session:
        print(resource_data)
        print(resource_data.model_dump())
        resource = ResourceModel(**resource_data.model_dump(exclude=("category", "quizes",)))
        session.add(resource)
        await session.commit()