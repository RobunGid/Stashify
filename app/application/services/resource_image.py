from application.services.base import BaseService
from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity
from domain.filters.resource_image import ResourceImageFilters


class ResourceImageService(BaseService[ResourceImageEntity, ResourceImageUpdateEntity, ResourceImageFilters]):
    pass
