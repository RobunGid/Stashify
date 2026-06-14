from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceFavoriteRepository(
    BaseRepository[ResourceFavoriteEntity, ResourceFavoriteUpdateEntity, ResourceFavoriteFilters],
    ABC,
):
    @abstractmethod
    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        pass
