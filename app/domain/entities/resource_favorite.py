from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class ResourceFavoriteEntity(BaseEntity):
    resource_favorite_id: UUID

    user_account_id: str
    resource_item_id: UUID


@dataclass
class ResourceFavoriteUpdateEntity(BaseUpdateEntity):
    user_account_id: str
    resource_item_id: UUID
