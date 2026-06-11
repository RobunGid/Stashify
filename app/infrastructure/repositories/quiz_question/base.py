from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseQuizQuestionRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_one(self, quiz_question_id: UUID) -> QuizQuestionEntity | None:
        pass

    @abstractmethod
    async def get_many(self, quiz_question_id: UUID) -> list[QuizQuestionEntity]:
        pass

    @abstractmethod
    async def create(self, quiz_question: QuizQuestionEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, quiz_question_id: UUID) -> None:
        pass

    @abstractmethod
    async def update(self, quiz_question_id: UUID, quiz_question: QuizQuestionUpdateEntity) -> None:
        pass
