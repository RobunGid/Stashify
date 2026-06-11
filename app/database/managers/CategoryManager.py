from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models.category import CategoryModel
from database.models.favorite import FavoriteModel
from database.models.quiz import QuizModel
from database.models.resource_item import ResourceItemModel
from database.orm import AsyncSessionLocal
from schemas.category_item_schema import CategoryItemSchema

from .BaseManager import BaseManager


class CategoryManager(BaseManager):
    model = CategoryModel
    schema = CategoryItemSchema

    @classmethod
    async def get_many(
        cls,
        has_quizes: bool = False,
        has_resources: bool = False,
        favorites_user_id: Optional[str] = None,
    ) -> List[CategoryItemSchema]:
        async with AsyncSessionLocal() as session:
            statement = select(CategoryModel).options(
                selectinload(CategoryModel.resource_items)
                .selectinload(ResourceItemModel.quiz)
                .selectinload(QuizModel.questions),
            )
            if has_quizes:
                subquery = (
                    select(ResourceItemModel.category_id)
                    .select_from(QuizModel)
                    .outerjoin(
                        ResourceItemModel,
                        ResourceItemModel.resource_item_id == QuizModel.resource_item_id,
                    )
                    .join(
                        CategoryModel,
                        CategoryModel.category_id == ResourceItemModel.category_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            if has_resources:
                subquery = (
                    select(ResourceItemModel.category_id)
                    .select_from(CategoryModel)
                    .outerjoin(
                        ResourceItemModel,
                        ResourceItemModel.category_id == CategoryModel.category_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            if favorites_user_id:
                subquery = (
                    select(ResourceItemModel.category_id)
                    .select_from(CategoryModel)
                    .outerjoin(
                        ResourceItemModel,
                        ResourceItemModel.category_id == CategoryModel.category_id,
                    )
                    .outerjoin(
                        FavoriteModel,
                        FavoriteModel.resource_item_id == ResourceItemModel.resource_item_id,
                    )
                    .where(
                        FavoriteModel.user_id == favorites_user_id,
                    )
                )
                statement = statement.where(CategoryModel.category_id.in_(subquery))

            categories = (await session.execute(statement)).scalars().all()
            return [CategoryItemSchema.model_validate(category, from_attributes=True) for category in categories]
