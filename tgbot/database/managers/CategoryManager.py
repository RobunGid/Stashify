from typing import Optional, List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.category_schema import CategorySchema
from database.orm import AsyncSessionLocal
from database.models.category import CategoryModel
from database.models.resource import ResourceModel
from database.models.quiz import QuizModel
from database.models.favorite import FavoriteModel

class CategoryManager:
    @classmethod
    async def create(cls, category_data: CategorySchema):
        async with AsyncSessionLocal() as session:
            category = CategoryModel(**category_data.model_dump())
            session.add(category)
            await session.commit()
    @classmethod
    async def edit_category(cls, id: UUID4, new_name: str) -> None:
        async with AsyncSessionLocal() as session:
            statement = select(CategoryModel).where(CategoryModel.id==id)
            category = (await session.execute(statement)).scalars().first()
            if not category:
                raise ValueError("No such category")
            category.name = new_name # type: ignore
            await session.commit()
    @classmethod
    async def get_categories(cls, has_quizes: bool = False, has_resources: bool = False, favorites_user_id: Optional[str] = None) -> List[CategorySchema]:
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
                statement = statement\
                    .where(CategoryModel.id.in_(subquery))    

            if favorites_user_id:
                subquery = select(ResourceModel.category_id)\
                    .select_from(CategoryModel)\
                    .outerjoin(
                        ResourceModel, ResourceModel.category_id == CategoryModel.id
                    )\
                    .outerjoin(
                        FavoriteModel, FavoriteModel.resource_id == ResourceModel.id
                    )\
                    .where(
                        FavoriteModel.user_id == favorites_user_id
                    )
                statement = statement\
                    .where(CategoryModel.id.in_(subquery))  

            categories = (await session.execute(statement)).scalars().all()
            return [CategorySchema.model_validate(category, from_attributes=True) for category in categories]
    @classmethod
    async def delete_category(cls, id: UUID4) -> None:
        async with AsyncSessionLocal() as session:
            statement = select(CategoryModel).where(CategoryModel.id==id)
            category = (await session.execute(statement)).scalars().first()
            if not category:
                raise ValueError("No such category")
            await session.delete(category)
            await session.commit()