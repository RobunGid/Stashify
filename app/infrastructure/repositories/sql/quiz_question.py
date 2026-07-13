from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters
from domain.repositories.quiz_question import BaseQuizQuestionRepository
from infrastructure.mappers.quiz_question import QuizQuestionMapper
from infrastructure.models.quiz_question import QuizQuestionModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import and_, func, select, update


@dataclass
class SQLQuizQuestionRepository(BaseQuizQuestionRepository, SQLAlchemyRepositoryMixin):
    async def create(self, quiz_question_entity: QuizQuestionEntity) -> None:
        quiz_question_model = QuizQuestionMapper.to_model(quiz_question_entity)
        self.session.add(quiz_question_model)
        await self.session.commit()

    async def get_one(self, quiz_question_id: UUID) -> QuizQuestionEntity | None:
        statement = select(QuizQuestionModel).where(
            QuizQuestionModel.quiz_question_id == quiz_question_id,
        )

        quiz_question_model = (await self.session.execute(statement)).scalars().first()

        if quiz_question_model is None:
            return None

        return QuizQuestionMapper.to_entity(quiz_question_model)

    async def get_many(self, filters: QuizQuestionFilters) -> GetManyResult[QuizQuestionEntity]:

        statement = select(QuizQuestionModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        quiz_question_models = (await self.session.execute(statement)).scalars().all()
        quiz_questions_entities = [
            QuizQuestionEntity(**quiz_question_model) for quiz_question_model in quiz_question_models
        ]
        return GetManyResult(items=quiz_questions_entities, total=total)

    async def delete_by_id(self, quiz_question_id: UUID) -> None:
        statement = select(QuizQuestionModel).where(QuizQuestionModel.quiz_question_id == quiz_question_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_question_id: UUID, quiz_question: QuizQuestionUpdateEntity) -> None:
        statement = (
            update(QuizQuestionModel)
            .where(QuizQuestionModel.quiz_question_id == quiz_question_id)
            .values(**{k: v for k, v in asdict(quiz_question).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def delete_by_question_number(self, resource_item_id: UUID, quiz_question_number: int) -> None:
        statement = select(QuizQuestionModel).where(
            and_(
                QuizQuestionModel.resource_item_id == resource_item_id,
                QuizQuestionModel.index == quiz_question_number,
            ),
        )
        quiz_question_model = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(quiz_question_model)
        await self.session.commit()

    async def get_one_by_question_number(
        self,
        resource_item_id: UUID,
        quiz_question_number: int,
    ) -> QuizQuestionEntity | None:
        statement = select(QuizQuestionModel).where(
            and_(
                QuizQuestionModel.resource_item_id == resource_item_id,
                QuizQuestionModel.quiz_question_number == quiz_question_number,
            ),
        )

        quiz_question_model = (await self.session.execute(statement)).scalars().first()

        if quiz_question_model is None:
            return None

        return QuizQuestionMapper.to_entity(quiz_question_model)

    async def get_count_by_quiz_item_id(self, quiz_item_id: UUID) -> int:
        statement = select(QuizQuestionModel).where(QuizQuestionModel.quiz_item_id == quiz_item_id)
        count_statement = select(func.count()).select_from(statement.subquery())

        total = (await self.session.execute(count_statement)).scalar_one()
        return total

    async def get_count(self, filters: QuizQuestionFilters) -> int:

        statement = select(QuizQuestionModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
