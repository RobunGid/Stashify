from uuid import UUID

from domain.entities.resource_favorite import ResourceFavoriteEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.resource_favorite import ResourceFavoriteModel


class ResourceFavoriteMapper(BaseMapper[ResourceFavoriteEntity, ResourceFavoriteModel]):
    @staticmethod
    def to_entity(model: ResourceFavoriteModel) -> ResourceFavoriteEntity:
        return ResourceFavoriteEntity(
            resource_favorite_id=UUID(str(model.resource_favorite_id)),
            user_account_id=UUID(str(model.user_account_id)),
            resource_item_id=UUID(str(model.resource_item_id)),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: ResourceFavoriteEntity) -> ResourceFavoriteModel:
        return ResourceFavoriteModel(
            resource_favorite_id=entity.resource_favorite_id,
            user_account_id=entity.user_account_id,
            resource_item_id=entity.resource_item_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
