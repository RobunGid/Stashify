from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters
from domain.repositories.quiz_item import BaseQuizItemRepository
from infrastructure.mappers.quiz_item import QuizItemMapper
from infrastructure.models.quiz_item import QuizItemModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import exists, func, select, update


@dataclass
class SQLQuizItemRepository(BaseQuizItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, quiz_item_entity: QuizItemEntity) -> None:
        model = QuizItemMapper.to_model(quiz_item_entity)
        self.session.add(model)
        await self.session.commit()

    async def get_one(self, quiz_item_id: UUID) -> QuizItemEntity | None:
        statement = select(QuizItemModel).where(
            QuizItemModel.quiz_item_id == quiz_item_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return QuizItemEntity(**item)

    async def get_many(self, filters: QuizItemFilters) -> GetManyResult[QuizItemEntity]:

        statement = select(QuizItemModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        quiz_item_models = (await self.session.execute(statement)).scalars().all()
        quiz_items_entities = [QuizItemMapper.to_entity(quiz_item_model) for quiz_item_model in quiz_item_models]
        return GetManyResult(items=quiz_items_entities, total=total)

    async def delete_by_id(self, quiz_item_id: UUID) -> None:
        statement = select(QuizItemModel).where(QuizItemModel.quiz_item_id == quiz_item_id)
        quiz_item_model = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(quiz_item_model)
        await self.session.commit()

    async def update(self, quiz_item_id: UUID, quiz_item: QuizItemUpdateEntity) -> None:
        statement = (
            update(QuizItemModel)
            .where(QuizItemModel.quiz_item_id == quiz_item_id)
            .values(**{k: v for k, v in asdict(quiz_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_one_by_resource_item_id(self, resource_item_id: UUID) -> QuizItemEntity | None:
        statement = select(QuizItemModel).where(
            QuizItemModel.resource_item_id == resource_item_id,
        )

        quiz_item_model = (await self.session.execute(statement)).scalars().first()

        if quiz_item_model is None:
            return None

        return QuizItemMapper.to_entity(quiz_item_model)

    async def check_exists_by_resource_item_id(self, resource_item_id: UUID) -> bool:
        statement = select(
            exists().where(
                QuizItemModel.resource_item_id == resource_item_id,
            ),
        )

        is_exists = (await self.session.execute(statement)).scalars().first()

        return bool(is_exists)

    async def get_count(self, filters: QuizItemFilters) -> int:
        statement = select(QuizItemModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
