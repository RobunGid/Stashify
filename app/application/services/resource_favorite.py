from application.services.base import BaseService
from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters


class ResourceFavoriteService(
    BaseService[ResourceFavoriteEntity, ResourceFavoriteUpdateEntity, ResourceFavoriteFilters]
):
    pass
