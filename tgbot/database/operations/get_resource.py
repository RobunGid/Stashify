from sqlalchemy import select
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from schemas.resource_schema import ResourceSchema

async def get_resource(resource_id: UUID4) -> ResourceSchema | None:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel)\
        .where(
            ResourceModel.id == resource_id
        )
        
        resource = (await session.execute(statement)).scalars().first()
        
        if resource is None:
            return None
        
        return ResourceSchema.model_validate(resource, from_attributes=True)