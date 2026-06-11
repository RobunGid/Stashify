from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseQuizResultRepository(BaseRepository, ABC):
    @abstractmethod
    def get_one(self, quiz_result_id: UUID) -> QuizResultEntity:
        pass

    @abstractmethod
    def get_many(self, quiz_result_id: UUID) -> list[QuizResultEntity]:
        pass

    @abstractmethod
    def create(self, quiz_result: QuizResultEntity) -> None:
        pass

    @abstractmethod
    def delete(self, quiz_result_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, quiz_result_id: UUID, quiz_result: QuizResultUpdateEntity) -> None:
        pass
