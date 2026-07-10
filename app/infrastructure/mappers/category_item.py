from uuid import UUID

from domain.entities.category_item import CategoryItemEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.category_item import CategoryItemModel


class CategoryItemMapper(BaseMapper[CategoryItemEntity, CategoryItemModel]):
    @staticmethod
    def to_entity(model: CategoryItemModel) -> CategoryItemEntity:
        return CategoryItemEntity(
            category_item_id=UUID(str(model.category_item_id)),
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
            resource_item_count=model.resource_item_count,
        )

    @staticmethod
    def to_model(entity: CategoryItemEntity) -> CategoryItemModel:
        return CategoryItemModel(
            category_item_id=entity.category_item_id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
