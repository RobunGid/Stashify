from abc import ABC

from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters
from infrastructure.repositories.base import BaseRepository


class BaseQuizItemRepository(BaseRepository[QuizItemEntity, QuizItemUpdateEntity, QuizItemFilters], ABC):
    pass
