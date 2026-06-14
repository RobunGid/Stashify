from uuid import UUID

from application.services.base import BaseService
from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from domain.filters.quiz_result import QuizResultFilters
from domain.repositories.quiz_result import BaseQuizResultRepository


class QuizResultService(BaseService[QuizResultEntity, QuizResultUpdateEntity, QuizResultFilters]):
    repository: BaseQuizResultRepository

    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        await self.repository.delete_by_user_account_id_and_resource_item_id(user_account_id, resource_item_id)

    async def get_one_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        await self.repository.get_one_by_user_account_id_and_resource_item_id(user_account_id, resource_item_id)
