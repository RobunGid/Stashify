from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models.category import CategoryModel
from database.models.favorite import FavoriteModel
from database.models.quiz import QuizModel
from database.models.resource import ResourceModel
from database.orm import AsyncSessionLocal
from schemas.category_schema import CategorySchema

from .BaseManager import BaseManager


class CategoryManager(BaseManager):
    model = CategoryModel
    schema = CategorySchema

    @classmethod
    async def get_many(
        cls,
        has_quizes: bool = False,
        has_resources: bool = False,
        favorites_user_id: Optional[str] = None,
    ) -> List[CategorySchema]:
        async with AsyncSessionLocal() as session:
            statement = select(CategoryModel).options(
                selectinload(CategoryModel.resources)
                .selectinload(ResourceModel.quiz)
                .selectinload(QuizModel.questions),
            )
            if has_quizes:
                subquery = (
                    select(ResourceModel.category_id)
                    .select_from(QuizModel)
                    .outerjoin(
                        ResourceModel,
                        ResourceModel.resource_id == QuizModel.resource_id,
                    )
                    .join(
                        CategoryModel,
                        CategoryModel.category_id == ResourceModel.category_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            if has_resources:
                subquery = (
                    select(ResourceModel.category_id)
                    .select_from(CategoryModel)
                    .outerjoin(
                        ResourceModel,
                        ResourceModel.category_id == CategoryModel.category_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            if favorites_user_id:
                subquery = (
                    select(ResourceModel.category_id)
                    .select_from(CategoryModel)
                    .outerjoin(
                        ResourceModel,
                        ResourceModel.category_id == CategoryModel.category_id,
                    )
                    .outerjoin(
                        FavoriteModel,
                        FavoriteModel.resource_id == ResourceModel.resource_id,
                    )
                    .where(
                        FavoriteModel.user_id == favorites_user_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            categories = (await session.execute(statement)).scalars().all()
            return [CategorySchema.model_validate(category, from_attributes=True) for category in categories]
