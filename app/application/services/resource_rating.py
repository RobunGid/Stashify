from application.services.base import BaseService
from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters


class ResourceRatingService(BaseService[ResourceRatingEntity, ResourceRatingUpdateEntity, ResourceRatingFilters]):
    pass
