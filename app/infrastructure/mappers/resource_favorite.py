from uuid import UUID

from domain.entities.resource_favorite import ResourceFavoriteEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.resource_favorite import ResourceFavoriteModel


class ResourceFavoriteMapper(BaseMapper[ResourceFavoriteEntity, ResourceFavoriteModel]):
    def to_entity(self, model: ResourceFavoriteModel) -> ResourceFavoriteEntity:
        return ResourceFavoriteEntity(
            resource_favorite_id=UUID(model.resource_favorite_id),
            user_account_id=UUID(model.user_account_id),
            resource_item_id=UUID(model.resource_item_id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: ResourceFavoriteEntity) -> ResourceFavoriteModel:
        return ResourceFavoriteModel(
            resource_favorite_id=entity.resource_favorite_id,
            user_account_id=entity.user_account_id,
            resource_item_id=entity.resource_item_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
