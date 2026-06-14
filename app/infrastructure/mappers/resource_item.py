from uuid import UUID

from domain.entities.resource_item import ResourceItemEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.resource_item import ResourceItemModel


class ResourceItemMapper(BaseMapper[ResourceItemEntity, ResourceItemModel]):
    @staticmethod
    def to_entity(model: ResourceItemModel) -> ResourceItemEntity:
        return ResourceItemEntity(
            resource_item_id=UUID(model.resource_item_id),
            name=model.name,
            description=model.description,
            links=model.links,
            tags=model.tags,
            verified=model.verified,
            category_item_id=UUID(model.category_item_id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: ResourceItemEntity) -> ResourceItemModel:
        return ResourceItemModel(
            resource_item_id=entity.resource_item_id,
            name=entity.name,
            description=entity.description,
            links=entity.links,
            tags=entity.tags,
            verified=entity.verified,
            category_item_id=entity.category_item_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
