from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from domain.filters.quiz_result import QuizResultFilters
from domain.repositories.quiz_result import BaseQuizResultRepository
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_result import QuizResultModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import func, select, update


@dataclass
class SQLQuizResultRepository(BaseQuizResultRepository, SQLAlchemyRepositoryMixin):
    async def create(self, quiz_result: QuizResultEntity) -> None:
        item = QuizResultModel(quiz_result)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, quiz_result_id: UUID) -> QuizResultEntity | None:
        statement = select(CategoryItemModel).where(
            QuizResultModel.quiz_result_id == quiz_result_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return QuizResultEntity(**item)

    async def get_many(self, filters: QuizResultFilters) -> GetManyResult[QuizResultEntity]:

        statement = select(QuizResultModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        quiz_results = (await self.session.execute(statement)).scalars().all()
        quiz_results_entities = [QuizResultEntity(**category) for category in quiz_results]
        return GetManyResult(items=quiz_results_entities, total=total)

    async def delete_by_id(self, quiz_result_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.quiz_result_id == quiz_result_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_result_id: UUID, quiz_result: QuizResultUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.quiz_result_id == quiz_result_id)
            .values(**{k: v for k, v in asdict(quiz_result).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
