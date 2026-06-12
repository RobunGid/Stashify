from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizResultEntity(BaseEntity):
    quiz_result_id: UUID

    quiz_item_id: UUID
    user_account_id: str
    percent: int


@dataclass
class QuizResultUpdateEntity(BaseUpdateEntity):
    quiz_item_id: UUID | None
    user_account_id: str | None
    percent: int | None
