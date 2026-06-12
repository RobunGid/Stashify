from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class QuizItemEntity(BaseEntity):
    quiz_item_id: UUID
    resource_item_id: UUID


@dataclass
class QuizItemUpdateEntity(BaseUpdateEntity):
    resource_item_id: UUID | None
