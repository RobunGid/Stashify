from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_option import QuizOptionEntity, QuizOptionUpdateEntity
from domain.filters.quiz_option import QuizOptionFilters
from domain.repositories.quiz_option import BaseQuizOptionRepository
from infrastructure.mappers.quiz_option import QuizOptionMapper
from infrastructure.models.quiz_option import QuizOptionModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from infrastructure.repositories.sql.utils.apply_pagination import apply_pagination_to_statement
from sqlalchemy import func, select, update


@dataclass
class SQLQuizOptionRepository(BaseQuizOptionRepository, SQLAlchemyRepositoryMixin):
    async def create(self, quiz_option_entity: QuizOptionEntity) -> None:
        quiz_option_model = QuizOptionMapper.to_model(quiz_option_entity)
        self.session.add(quiz_option_model)
        await self.session.commit()

    async def get_one(self, quiz_option_id: UUID) -> QuizOptionEntity | None:
        statement = select(QuizOptionModel).where(
            QuizOptionModel.quiz_option_id == quiz_option_id,
        )

        quiz_option_model = (await self.session.execute(statement)).scalars().first()

        if quiz_option_model is None:
            return None

        return QuizOptionMapper.to_entity(quiz_option_model)

    async def get_many(self, filters: QuizOptionFilters) -> GetManyResult[QuizOptionEntity]:

        statement = select(QuizOptionModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        statement = apply_pagination_to_statement(statement, filters)

        quiz_option_models = (await self.session.execute(statement)).scalars().all()
        quiz_option_entities = [
            QuizOptionMapper.to_entity(quiz_option_model) for quiz_option_model in quiz_option_models
        ]
        return GetManyResult(items=quiz_option_entities, total=total)

    async def delete_by_id(self, quiz_option_id: UUID) -> None:
        statement = select(QuizOptionModel).where(QuizOptionModel.quiz_option_id == quiz_option_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_option_id: UUID, quiz_option_entity: QuizOptionUpdateEntity) -> None:
        statement = (
            update(QuizOptionModel)
            .where(QuizOptionModel.quiz_option_id == quiz_option_id)
            .values(**{k: v for k, v in asdict(quiz_option_entity).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_count(self, filters: QuizOptionFilters) -> int:

        statement = select(QuizOptionModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
