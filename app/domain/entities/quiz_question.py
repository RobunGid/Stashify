from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizQuestionEntity(BaseEntity):
    quiz_question_id: UUID
    text: str

    quiz_item_id: UUID

    image: str | None


@dataclass
class QuizQuestionUpdateEntity(BaseUpdateEntity):
    text: str | None

    image: str | None
