from domain.entities.category_item import CategoryItemEntity, CategoryItemUpdateEntity
from domain.filters.category_item import CategoryItemFilters
from domain.repositories.base import BaseRepository


class BaseCategoryItemRepository(BaseRepository[CategoryItemEntity, CategoryItemUpdateEntity, CategoryItemFilters]):
    pass
