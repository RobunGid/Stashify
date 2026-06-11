from abc import ABC

from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceFavoriteRepository(
    BaseRepository[ResourceFavoriteEntity, ResourceFavoriteUpdateEntity, ResourceFavoriteFilters], ABC
):
    pass
