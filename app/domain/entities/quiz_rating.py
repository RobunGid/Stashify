from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass
class QuizRatingEntity(BaseEntity):
    quiz_rating_id: str

    quiz_item_id: UUID
    user_account_id: str
    rating: int


@dataclass
class QuizRatingUpdateEntity(BaseEntity):
    quiz_item_id: UUID | None
    user_account_id: str | None
    rating: int | None
