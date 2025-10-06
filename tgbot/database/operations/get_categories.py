from typing import List, Optional

from sqlalchemy import outerjoin, select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from schemas.category_schema import CategorySchema

async def get_categories(has_quizes: bool = False, has_resources: bool = False) -> List[CategorySchema]:
    async with AsyncSessionLocal() as session:
        statement = select(CategoryModel)\
        .options(
            selectinload(CategoryModel.resources).selectinload(ResourceModel.quiz).selectinload(QuizModel.questions)
        )
        if has_quizes:
            subquery = select(ResourceModel.category_id)\
                .select_from(QuizModel)\
                .outerjoin(
                    ResourceModel, ResourceModel.id == QuizModel.resource_id
                )\
                .join(
                    CategoryModel, CategoryModel.id == ResourceModel.category_id
                )
            statement = statement.where(CategoryModel.id.in_(subquery))
            
        if has_resources:
            subquery = select(ResourceModel.category_id)\
                .select_from(CategoryModel)\
                .outerjoin(
                    ResourceModel, ResourceModel.category_id == CategoryModel.id
                )
            statement = statement.where(CategoryModel.id.in_(subquery))    

        categories = (await session.execute(statement)).scalars().all()
        
        return [CategorySchema.model_validate(category, from_attributes=True) for category in categories]