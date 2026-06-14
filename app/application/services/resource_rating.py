from uuid import UUID

from application.services.base import BaseService
from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters
from domain.repositories.resource_rating import BaseResourceRatingRepository


class ResourceRatingService(BaseService[ResourceRatingEntity, ResourceRatingUpdateEntity, ResourceRatingFilters]):
    repository: BaseResourceRatingRepository

    async def get_one_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> ResourceRatingEntity | None:
        return await self.repository.get_one_by_user_account_id_and_resource_item_id(user_account_id, resource_item_id)

    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        return await self.repository.delete_by_user_account_id_and_resource_item_id(user_account_id, resource_item_id)
