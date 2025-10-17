from typing import List, Optional
from sqlalchemy import func, or_, select, column
from sqlalchemy.orm import selectinload
from pydantic import UUID4

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from database.models.favorite import FavoriteModel
from schemas.resource_schema import ResourceSchema

FIND_COLUMNS = [ResourceModel.links, ResourceModel.description, ResourceModel.tags, ResourceModel.name]

async def get_resources(category_id: Optional[UUID4] = None, has_quiz: bool = False, text: Optional[str] = None, favorites_user_id: Optional[str] = None) -> List[ResourceSchema]:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel)\
        .options(
            selectinload(ResourceModel.category)
        )\
        .options(
            selectinload(ResourceModel.quiz).selectinload(QuizModel.questions)
        )
        
        if has_quiz:
            statement = statement.filter(ResourceModel.quiz != None)
        else:
            statement = statement.filter(ResourceModel.quiz == None)
            
        if category_id: 
            statement = statement.where(ResourceModel.category_id==category_id)
        
        if text:
            statement = statement.filter(
                or_(
                    *[func.lower(col).contains(text.lower()) for col in FIND_COLUMNS]
                )
            )
        
        if favorites_user_id:
            statement = statement.\
                join(FavoriteModel, FavoriteModel.resource_id == ResourceModel.id).\
                where(FavoriteModel.user_id == favorites_user_id)
        
        resources = (await session.execute(statement)).scalars().all()
        
        return [ResourceSchema.model_validate(resource, from_attributes=True) for resource in resources]