from dataclasses import dataclass, field
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class QuizQuestionFilters(BaseFilters):
    resource_item_id: UUID | None = field(kw_only=True)
    quiz_item_id: UUID | None = field(kw_only=True)
    count: int | None = None
