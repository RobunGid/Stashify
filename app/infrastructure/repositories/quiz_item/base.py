from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity


@dataclass
class BaseQuizItemRepository(ABC):
    @abstractmethod
    def get_one(self, quiz_item_id: UUID) -> QuizItemEntity:
        pass

    @abstractmethod
    def get_many(self, quiz_item_id: UUID) -> list[QuizItemEntity]:
        pass

    @abstractmethod
    def create(self, quiz_item: QuizItemEntity) -> None:
        pass

    @abstractmethod
    def delete(self, quiz_item_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, quiz_item_id: UUID, quiz_item: QuizItemUpdateEntity) -> None:
        pass
