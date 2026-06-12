from abc import ABC

from domain.entities.quiz_rating import QuizRatingEntity, QuizRatingUpdateEntity
from domain.filters.quiz_rating import QuizRatingFilters
from infrastructure.repositories.base import BaseRepository


class BaseQuizRatingRepository(BaseRepository[QuizRatingEntity, QuizRatingUpdateEntity, QuizRatingFilters], ABC):
    pass
