from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_rating import QuizRatingEntity, QuizRatingUpdateEntity
from domain.filters.quiz_rating import QuizRatingFilters
from domain.repositories.quiz_rating import BaseQuizRatingRepository
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_rating import QuizRatingModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import func, select, update


@dataclass
class SQLQuizRatingRepository(BaseQuizRatingRepository, SQLAlchemyRepositoryMixin):
    async def create(self, quiz_rating: QuizRatingEntity) -> None:
        item = QuizRatingModel(quiz_rating)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, quiz_rating_id: UUID) -> QuizRatingEntity | None:
        statement = select(CategoryItemModel).where(
            QuizRatingModel.quiz_rating_id == quiz_rating_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return QuizRatingEntity(**item)

    async def get_many(self, filters: QuizRatingFilters) -> GetManyResult[QuizRatingEntity]:

        statement = select(QuizRatingModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        quiz_ratings = (await self.session.execute(statement)).scalars().all()
        quiz_ratings_entities = [QuizRatingEntity(**category) for category in quiz_ratings]
        return GetManyResult(items=quiz_ratings_entities, total=total)

    async def delete_by_id(self, quiz_rating_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.quiz_rating_id == quiz_rating_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_rating_id: UUID, quiz_rating: QuizRatingUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.quiz_rating_id == quiz_rating_id)
            .values(**{k: v for k, v in asdict(quiz_rating).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_count(self, filters: QuizRatingFilters) -> int:

        statement = select(QuizRatingModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
