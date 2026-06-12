from uuid import UUID

from domain.entities.resource_image import ResourceImageEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.resource_image import ResourceImageModel


class ResourceImageMapper(BaseMapper[ResourceImageEntity, ResourceImageModel]):
    def to_entity(self, model: ResourceImageModel) -> ResourceImageEntity:
        return ResourceImageEntity(
            resource_image_id=UUID(model.resource_image_id),
            resource_item_id=UUID(model.resource_item_id),
            image=model.image,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: ResourceImageEntity) -> ResourceImageModel:
        return ResourceImageModel(
            resource_image_id=entity.resource_image_id,
            resource_item_id=entity.resource_item_id,
            image=entity.image,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
