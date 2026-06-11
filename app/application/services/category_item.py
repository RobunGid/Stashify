from application.services.base import BaseService
from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters


class CategoryItemService(BaseService[CategoryItemEntity, CategoryItemUpdateEntity, CategoryItemFilters]):
    pass
