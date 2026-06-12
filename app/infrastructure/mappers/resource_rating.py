from uuid import UUID

from domain.entities.resource_rating import ResourceRatingEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.resource_rating import ResourceRatingModel


class ResourceRatingMapper(BaseMapper[ResourceRatingEntity, ResourceRatingModel]):
    def to_entity(self, model: ResourceRatingModel) -> ResourceRatingEntity:
        return ResourceRatingEntity(
            resource_rating_id=UUID(model.resource_rating_id),
            resource_item_id=UUID(model.resource_item_id),
            user_account_id=UUID(model.user_account_id),
            rating=model.rating,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: ResourceRatingEntity) -> ResourceRatingModel:
        return ResourceRatingModel(
            resource_rating_id=entity.resource_rating_id,
            resource_item_id=entity.resource_item_id,
            user_account_id=entity.user_account_id,
            rating=entity.rating,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
