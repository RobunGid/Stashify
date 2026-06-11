from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from infrastructure.models.category import CategoryModel
from infrastructure.models.favorite import FavoriteModel
from infrastructure.models.quiz import QuizModel
from infrastructure.models.resource_item import ResourceItemModel
from infrastructure.repositories.base import SQLAlchemyRepositoryMixin
from infrastructure.repositories.category_item.base import BaseCategoryItemRepository
from sqlalchemy import select, Update
from sqlalchemy.orm import selectinload


@dataclass
class SQLCategoryItemRepository(BaseCategoryItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, category_item: CategoryItemEntity) -> None:
        item = CategoryModel(category_item)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, category_item_id: UUID) -> CategoryItemEntity | None:
        statement = select(CategoryModel).where(
            CategoryModel.category_item_id == category_item_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return CategoryItemEntity(**item)

    async def get_many(self, filters: CategoryItemFilters) -> list[CategoryItemEntity]:
        statement = select(CategoryModel).options(
            selectinload(CategoryModel.resource_items)
            .selectinload(ResourceItemModel.quiz)
            .selectinload(QuizModel.questions),
        )
        if filters.has_quiz_items:
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

        if filters.has_resource_items:
            subquery = (
                select(ResourceItemModel.category_id)
                .select_from(CategoryModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.category_id == CategoryModel.category_id,
                )
            )
            statement = statement.where(CategoryModel.category_id.in_(subquery))

        if filters.favorite_user_id:
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
                    FavoriteModel.user_id == filters.favorite_user_id,
                )
            )
            statement = statement.where(CategoryModel.category_id.in_(subquery))

        categories = (await self.session.execute(statement)).scalars().all()
        return [CategoryItemEntity(**category) for category in categories]

    async def delete(self, category_item_id: UUID) -> None:
        statement = select(CategoryModel).where(CategoryModel.category_item_id == category_item_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, category_item_id: UUID, category_item: CategoryItemUpdateEntity) -> None:
        statement = (
            Update(CategoryModel)
            .where(CategoryModel.category_item_id == category_item_id)
            .values(**{k: v for k, v in asdict(category_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
