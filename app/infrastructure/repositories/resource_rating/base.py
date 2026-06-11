from abc import ABC

from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters
from infrastructure.repositories.base import BaseRepository


class BaseResourceRatingRepository(
    BaseRepository[ResourceRatingEntity, ResourceRatingUpdateEntity, ResourceRatingFilters], ABC
):
    pass
