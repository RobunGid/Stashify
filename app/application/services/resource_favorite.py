from dataclasses import dataclass
from uuid import UUID

from application.services.base import BaseService
from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters
from domain.repositories.resource_favorite import BaseResourceFavoriteRepository


@dataclass
class ResourceFavoriteService(
    BaseService[ResourceFavoriteEntity, ResourceFavoriteUpdateEntity, ResourceFavoriteFilters],
):
    repository: BaseResourceFavoriteRepository

    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        await self.repository.delete_by_user_account_id_and_resource_item_id(user_account_id, resource_item_id)
