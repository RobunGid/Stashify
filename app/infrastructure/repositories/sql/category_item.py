from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from domain.repositories.category_item import BaseCategoryItemRepository
from infrastructure.mappers.category_item import CategoryItemMapper
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_item import QuizItemModel
from infrastructure.models.resource_favorite import ResourceFavoriteModel
from infrastructure.models.resource_item import ResourceItemModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload


@dataclass
class SQLCategoryItemRepository(BaseCategoryItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, category_item: CategoryItemEntity) -> None:
        model = CategoryItemModel.from_entity(category_item)
        self.session.add(model)
        await self.session.commit()

    async def get_one(self, category_item_id: UUID) -> CategoryItemEntity | None:
        statement = (
            select(CategoryItemModel)
            .options(selectinload(CategoryItemModel.resource_items))
            .where(
                CategoryItemModel.category_item_id == category_item_id,
            )
        )

        category_item_model = (await self.session.execute(statement)).scalars().first()

        if category_item_model is None:
            return None

        return CategoryItemMapper.to_entity(category_item_model)

    async def get_many(self, filters: CategoryItemFilters) -> GetManyResult[CategoryItemEntity]:

        statement = select(CategoryItemModel).options(
            selectinload(CategoryItemModel.resource_items)
            .selectinload(ResourceItemModel.quiz_item)
            .selectinload(QuizItemModel.quiz_questions),
        )
        if filters.has_resource_items is not None:
            subquery = (
                select(ResourceItemModel.category_item_id)
                .select_from(CategoryItemModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                )
            )
            if filters.has_resource_items is True:
                statement = statement.where(CategoryItemModel.category_item_id.in_(subquery))
            else:
                statement = statement.where(~CategoryItemModel.category_item_id.in_(subquery))

            if filters.has_quiz_items is not None:
                if filters.has_quiz_items:
                    quiz_exists = (
                        select(1)
                        .select_from(ResourceItemModel)
                        .join(
                            QuizItemModel,
                            QuizItemModel.resource_item_id == ResourceItemModel.resource_item_id,
                        )
                        .where(ResourceItemModel.category_item_id == CategoryItemModel.category_item_id)
                        .exists()
                    )
                    statement = statement.where(quiz_exists)
                else:
                    resource_without_quiz_exists = (
                        select(1)
                        .select_from(ResourceItemModel)
                        .outerjoin(
                            QuizItemModel,
                            QuizItemModel.resource_item_id == ResourceItemModel.resource_item_id,
                        )
                        .where(
                            ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                            QuizItemModel.quiz_item_id.is_(None),
                        )
                        .exists()
                    )
                    statement = statement.where(resource_without_quiz_exists)

        if filters.favorite_user_id is not None:
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

        category_item_models = (await self.session.execute(statement)).scalars().all()
        categories_entities = [
            CategoryItemMapper.to_entity(model=category_item_model) for category_item_model in category_item_models
        ]
        return GetManyResult(items=categories_entities, total=total)

    async def delete_by_id(self, category_item_id: UUID) -> None:
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

    async def get_count(self, filters: CategoryItemFilters) -> int:
        statement = select(CategoryItemModel).options(
            selectinload(CategoryItemModel.resource_items)
            .selectinload(ResourceItemModel.quiz_item)
            .selectinload(QuizItemModel.quiz_questions),
        )
        if filters.has_resource_items is not None:
            subquery = (
                select(ResourceItemModel.category_item_id)
                .select_from(CategoryItemModel)
                .outerjoin(
                    ResourceItemModel,
                    ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                )
            )
            if filters.has_resource_items is True:
                statement = statement.where(CategoryItemModel.category_item_id.in_(subquery))
            else:
                statement = statement.where(~CategoryItemModel.category_item_id.in_(subquery))

            if filters.has_quiz_items is not None:
                if filters.has_quiz_items:
                    quiz_exists = (
                        select(1)
                        .select_from(ResourceItemModel)
                        .join(
                            QuizItemModel,
                            QuizItemModel.resource_item_id == ResourceItemModel.resource_item_id,
                        )
                        .where(ResourceItemModel.category_item_id == CategoryItemModel.category_item_id)
                        .exists()
                    )
                    statement = statement.where(quiz_exists)
                else:
                    resource_without_quiz_exists = (
                        select(1)
                        .select_from(ResourceItemModel)
                        .outerjoin(
                            QuizItemModel,
                            QuizItemModel.resource_item_id == ResourceItemModel.resource_item_id,
                        )
                        .where(
                            ResourceItemModel.category_item_id == CategoryItemModel.category_item_id,
                            QuizItemModel.quiz_item_id.is_(None),
                        )
                        .exists()
                    )
                    statement = statement.where(resource_without_quiz_exists)

        if filters.favorite_user_id is not None:
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

        return total
