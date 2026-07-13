from dataclasses import dataclass, field
from uuid import UUID

from domain.filters.base import BaseFilters


@dataclass
class QuizOptionFilters(BaseFilters):
    quiz_question_id: UUID = field(kw_only=True)
