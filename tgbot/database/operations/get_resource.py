from typing import List, Optional
from sqlalchemy import select, column
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from schemas.resource_schema import ResourceSchema

async def get_resource(resource_id: UUID4) -> ResourceSchema | None:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel)\
        .options(
            selectinload(ResourceModel.category),
            selectinload(ResourceModel.quiz).selectinload(QuizModel.questions),
            selectinload(ResourceModel.ratings)	
        )\
        .where(
            ResourceModel.id == resource_id
        )
        
        resource = (await session.execute(statement)).scalars().first()
        
        if resource is None:
            return None
        
        _ = resource.quiz
        _ = resource.quiz.questions
        _ = resource.ratings
        
        return ResourceSchema.model_validate(resource, from_attributes=True)