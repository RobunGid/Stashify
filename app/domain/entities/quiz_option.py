from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizOptionEntity(BaseEntity):
    quiz_question_id: UUID

    text: str
    is_right: bool


@dataclass
class QuizOptionUpdateEntity(BaseUpdateEntity):
    text: str | None = None
    is_right: bool | None = None
