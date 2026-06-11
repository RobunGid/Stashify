from abc import ABC, abstractmethod

from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceItemRepository(
    BaseRepository[ResourceItemEntity, ResourceItemUpdateEntity, ResourceItemFilters], ABC
):
    @abstractmethod
    async def get_one_by_telegram_id(self, telegram_id: int) -> ResourceItemEntity | None:
        pass
