from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseResourceRatingRepository(BaseRepository, ABC):
    @abstractmethod
    def get_one(self, resource_rating_id: UUID) -> ResourceRatingEntity:
        pass

    @abstractmethod
    def get_many(self, resource_rating_id: UUID) -> list[ResourceRatingEntity]:
        pass

    @abstractmethod
    def create(self, resource_rating: ResourceRatingEntity) -> None:
        pass

    @abstractmethod
    def delete(self, resource_rating_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, resource_rating_id: UUID, resource_rating: ResourceRatingUpdateEntity) -> None:
        pass
