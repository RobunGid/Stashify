from dataclasses import dataclass
from uuid import UUID

from application.services.base import BaseService
from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters
from domain.repositories.quiz_question import BaseQuizQuestionRepository


@dataclass
class QuizQuestionService(BaseService[QuizQuestionEntity, QuizQuestionUpdateEntity, QuizQuestionFilters]):
    repository: BaseQuizQuestionRepository

    async def delete_by_question_number(self, resource_item_id: UUID, quiz_question_number: int) -> None:
        return await self.repository.delete_by_question_number(resource_item_id, quiz_question_number)

    async def get_one_by_question_number(
        self,
        resource_item_id: UUID,
        quiz_question_number: int,
    ) -> QuizQuestionEntity | None:
        return await self.repository.get_one_by_question_number(resource_item_id, quiz_question_number)

    async def get_count_by_quiz_item_id(self, quiz_item_id: UUID) -> int:
        return await self.repository.get_count_by_quiz_item_id(quiz_item_id)
