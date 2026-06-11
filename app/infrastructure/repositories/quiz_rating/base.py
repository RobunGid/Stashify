from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.quiz_rating import QuizRatingEntity, QuizRatingUpdateEntity


@dataclass
class BaseQuizRatingRepository(ABC):
    @abstractmethod
    def get_one(self, quiz_rating_id: UUID) -> QuizRatingEntity:
        pass

    @abstractmethod
    def get_many(self, quiz_rating_id: UUID) -> list[QuizRatingEntity]:
        pass

    @abstractmethod
    def create(self, quiz_rating: QuizRatingEntity) -> None:
        pass

    @abstractmethod
    def delete(self, quiz_rating_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, quiz_rating_id: UUID, quiz_rating: QuizRatingUpdateEntity) -> None:
        pass
