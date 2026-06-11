from abc import ABC

from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from domain.filters.quiz_result import QuizResultFilters
from infrastructure.repositories.base import BaseRepository


class BaseQuizResultRepository(BaseRepository[QuizResultEntity, QuizResultUpdateEntity, QuizResultFilters], ABC):
    pass
