from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters
from domain.repositories.base import BaseRepository


class BaseQuizQuestionRepository(
    BaseRepository[QuizQuestionEntity, QuizQuestionUpdateEntity, QuizQuestionFilters],
    ABC,
):
    @abstractmethod
    async def delete_by_question_number(self, resource_item_id: UUID, quiz_question_number: int) -> None:
        pass

    @abstractmethod
    async def get_one_by_question_number(
        self,
        resource_item_id: UUID,
        quiz_question_number: int,
    ) -> QuizQuestionEntity | None:
        pass

    @abstractmethod
    async def get_count_by_quiz_item_id(self, quiz_item_id: UUID) -> int:
        pass
