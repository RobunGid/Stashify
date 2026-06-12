from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizRatingEntity(BaseEntity):
    quiz_rating_id: UUID

    quiz_item_id: UUID
    user_account_id: UUID
    rating: int


@dataclass
class QuizRatingUpdateEntity(BaseUpdateEntity):
    quiz_item_id: UUID | None
    user_account_id: UUID | None
    rating: int | None
