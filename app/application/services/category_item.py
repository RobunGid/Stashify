from application.services.base import BaseService
from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from domain.repositories.category_item import BaseCategoryItemRepository


class CategoryItemService(BaseService[CategoryItemEntity, CategoryItemUpdateEntity, CategoryItemFilters]):
    repository: BaseCategoryItemRepository
