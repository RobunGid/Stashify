from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from database.models.resource import ResourceModel
from schemas.resource_schema import ResourceSchema

async def get_resources() -> List[ResourceSchema]:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel)\
        .options(
            selectinload(ResourceModel.category)
		)\
        .options(
			selectinload(ResourceModel.quizes)
		)
        resources = (await session.execute(statement)).scalars().all()
        
        return [ResourceSchema.model_validate(resource, from_attributes=True) for resource in resources]