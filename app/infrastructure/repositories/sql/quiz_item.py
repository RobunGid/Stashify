from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_item import QuizItemModel
from infrastructure.repositories.base import BaseSQLAlchemyRepository
from sqlalchemy import func, select, update


@dataclass
class SQLQuizItemRepository(BaseSQLAlchemyRepository[QuizItemEntity, QuizItemUpdateEntity, QuizItemFilters]):
    async def create(self, quiz_item: QuizItemEntity) -> None:
        item = QuizItemModel(quiz_item)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, quiz_item_id: UUID) -> QuizItemEntity | None:
        statement = select(CategoryItemModel).where(
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

        quiz_items = (await self.session.execute(statement)).scalars().all()
        quiz_items_entities = [QuizItemEntity(**category) for category in quiz_items]
        return GetManyResult(items=quiz_items_entities, total=total)

    async def delete(self, quiz_item_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.quiz_item_id == quiz_item_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_item_id: UUID, quiz_item: QuizItemUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.quiz_item_id == quiz_item_id)
            .values(**{k: v for k, v in asdict(quiz_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
