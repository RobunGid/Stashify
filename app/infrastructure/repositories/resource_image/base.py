from abc import ABC

from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity
from domain.filters.resource_image import ResourceImageFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceImageRepository(
    BaseRepository[ResourceImageEntity, ResourceImageUpdateEntity, ResourceImageFilters],
    ABC,
):
    pass
