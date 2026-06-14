from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters
from infrastructure.repositories.base import BaseRepository


class BaseQuizItemRepository(BaseRepository[QuizItemEntity, QuizItemUpdateEntity, QuizItemFilters], ABC):
    @abstractmethod
    async def get_one_by_resource_item_id(self, resource_item_id: UUID) -> QuizItemEntity | None:
        pass
