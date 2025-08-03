from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from database.models.resource import ResourceModel
from schemas.resource_schema import ResourceSchema

async def get_resources(category_id: Optional[UUID4] = None) -> List[ResourceSchema]:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel)\
        .options(
            selectinload(ResourceModel.category)
        )\
        .options(
            selectinload(ResourceModel.quizes)
        )
        if category_id: 
            statement = statement.where(ResourceModel.category_id==category_id)
        
        resources = (await session.execute(statement)).scalars().all()
        
        return [ResourceSchema.model_validate(resource, from_attributes=True) for resource in resources]