from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity


@dataclass
class BaseResourceFavoriteRepository(ABC):
    @abstractmethod
    def get_one(self, resource_favorite_id: UUID) -> ResourceFavoriteEntity:
        pass

    @abstractmethod
    def get_many(self, resource_favorite_id: UUID) -> list[ResourceFavoriteEntity]:
        pass

    @abstractmethod
    def create(self, resource_favorite: ResourceFavoriteEntity) -> None:
        pass

    @abstractmethod
    def delete(self, resource_favorite_id: UUID) -> None:
        pass

    @abstractmethod
    def update(self, resource_favorite_id: UUID, resource_favorite: ResourceFavoriteUpdateEntity) -> None:
        pass
