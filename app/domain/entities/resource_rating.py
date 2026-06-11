from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass
class ResourceRatingEntity(BaseEntity):
    resource_rating_id: UUID

    resource_item_id: UUID

    user_id: str

    rating: int


@dataclass
class ResourceRatingUpdateEntity(BaseEntity):
    resource_item_id: UUID | None

    user_id: str | None

    rating: int | None
