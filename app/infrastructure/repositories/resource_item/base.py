from abc import ABC

from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceItemRepository(
    BaseRepository[ResourceItemEntity, ResourceItemUpdateEntity, ResourceItemFilters],
    ABC,
):
    pass
