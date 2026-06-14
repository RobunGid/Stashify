from dataclasses import dataclass
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class QuizQuestionFilters(BaseFilters):
    resource_item_id: UUID
    count: int | None = None
