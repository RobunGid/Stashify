from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizQuestionEntity(BaseEntity):
    quiz_question_id: UUID
    text: str

    quiz_item_id: UUID

    options: list[str]
    right_options: list[int]

    image: str | None


@dataclass
class QuizQuestionUpdateEntity(BaseUpdateEntity):
    text: str | None

    options: list[str] | None
    right_options: list[int] | None

    image: str | None
