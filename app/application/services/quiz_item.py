from uuid import UUID

from application.services.base import BaseService
from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters
from domain.repositories.quiz_item import BaseQuizItemRepository


class QuizItemService(BaseService[QuizItemEntity, QuizItemUpdateEntity, QuizItemFilters]):
    repository: BaseQuizItemRepository

    async def get_one_by_resource_item_id(self, resource_item_id: UUID) -> QuizItemEntity | None:
        return await self.repository.get_one_by_resource_item_id(resource_item_id)

    async def check_exists_by_resource_item_id(self, resource_item_id: UUID) -> bool:
        return await self.repository.check_exists_by_resource_item_id(resource_item_id)
