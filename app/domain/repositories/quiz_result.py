from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from domain.filters.quiz_result import QuizResultFilters
from domain.repositories.base import BaseRepository


class BaseQuizResultRepository(BaseRepository[QuizResultEntity, QuizResultUpdateEntity, QuizResultFilters], ABC):
    @abstractmethod
    async def get_one_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> QuizResultEntity | None:
        pass

    @abstractmethod
    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        pass
