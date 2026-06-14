from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters
from domain.repositories.base import BaseRepository


class BaseResourceRatingRepository(
    BaseRepository[ResourceRatingEntity, ResourceRatingUpdateEntity, ResourceRatingFilters],
    ABC,
):
    @abstractmethod
    async def get_one_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> ResourceRatingEntity | None:
        pass

    @abstractmethod
    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        pass
