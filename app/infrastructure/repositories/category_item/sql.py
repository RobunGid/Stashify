from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_item import QuizItemModel
from infrastructure.models.resource_favorite import ResourceFavoriteModel
from infrastructure.models.resource_item import ResourceItemModel
from infrastructure.repositories.base import GetManyResult, SQLAlchemyRepositoryMixin
from infrastructure.repositories.category_item.base import BaseCategoryItemRepository
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload


@dataclass
class SQLCategoryItemRepository(BaseCategoryItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, category_item: CategoryItemEntity) -> None:
        model = CategoryItemModel.from_entity(category_item)
        self.session.add(model)
        await self.session.commit()

    async def get_one(self, category_item_id: UUID) -> CategoryItemEntity | None:
        statement = select(CategoryItemModel).where(
            CategoryItemModel.category_item_id == category_item_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return CategoryItemEntity(**item)

    async def get_many(self, filters: CategoryItemFilters) -> GetManyResult[CategoryItemEntity]:

        statement = select(CategoryItemModel).options(
            selectinload(CategoryItemModel.resource_items)
            .selectinload(ResourceItemModel.quiz)
            .selectinload(QuizItemModel.questions),
        )
        if filters.has_quiz_items:
            subquery = (
                select(ResourceItemModel.category_item_id)
                .select_from(QuizItemModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.resource_item_id == QuizItemModel.resource_item_id,
                )
                .join(
                    CategoryItemModel,
                    CategoryItemModel.category_item_id == ResourceItemModel.category_item_id,
                )
            )
            statement = statement.where(CategoryItemModel.category_item_id.in_(subquery))

        if filters.has_resource_items:
            subquery = (
                select(ResourceItemModel.category_item_id)
                .select_from(CategoryItemModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                )
            )
            statement = statement.where(CategoryItemModel.category_item_id.in_(subquery))

        if filters.favorite_user_id:
            subquery = (
                select(ResourceItemModel.category_item_id)
                .select_from(CategoryItemModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                )
                .outerjoin(
                    ResourceFavoriteModel,
                    ResourceFavoriteModel.resource_item_id == ResourceItemModel.resource_item_id,
                )
                .where(
                    ResourceFavoriteModel.user_account_id == filters.favorite_user_id,
                )
            )
            statement = statement.where(CategoryItemModel.category_item_id.in_(subquery))

        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        categories = (await self.session.execute(statement)).scalars().all()
        categories_entities = [CategoryItemEntity(**category) for category in categories]
        return GetManyResult(items=categories_entities, total=total)

    async def delete(self, category_item_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.category_item_id == category_item_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, category_item_id: UUID, category_item: CategoryItemUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.category_item_id == category_item_id)
            .values(**{k: v for k, v in asdict(category_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
