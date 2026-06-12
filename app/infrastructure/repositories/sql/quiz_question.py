from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.quiz_question import QuizQuestionModel
from infrastructure.repositories.base import BaseSQLAlchemyRepository
from sqlalchemy import func, select, update


@dataclass
class SQLQuizQuestionRepository(
    BaseSQLAlchemyRepository[QuizQuestionEntity, QuizQuestionUpdateEntity, QuizQuestionFilters]
):
    async def create(self, quiz_question: QuizQuestionEntity) -> None:
        item = QuizQuestionModel(quiz_question)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, quiz_question_id: UUID) -> QuizQuestionEntity | None:
        statement = select(CategoryItemModel).where(
            QuizQuestionModel.quiz_question_id == quiz_question_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return QuizQuestionEntity(**item)

    async def get_many(self, filters: QuizQuestionFilters) -> GetManyResult[QuizQuestionEntity]:

        statement = select(QuizQuestionModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        quiz_questions = (await self.session.execute(statement)).scalars().all()
        quiz_questions_entities = [QuizQuestionEntity(**category) for category in quiz_questions]
        return GetManyResult(items=quiz_questions_entities, total=total)

    async def delete(self, quiz_question_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.quiz_question_id == quiz_question_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, quiz_question_id: UUID, quiz_question: QuizQuestionUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.quiz_question_id == quiz_question_id)
            .values(**{k: v for k, v in asdict(quiz_question).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
