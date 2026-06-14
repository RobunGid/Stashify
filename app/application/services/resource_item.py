from application.services.base import BaseService
from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from domain.repositories.resource_item import BaseResourceItemRepository


class ResourceItemService(BaseService[ResourceItemEntity, ResourceItemUpdateEntity, ResourceItemFilters]):
    repository: BaseResourceItemRepository
