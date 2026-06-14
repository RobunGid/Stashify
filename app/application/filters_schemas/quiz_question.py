from dataclasses import dataclass
from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.quiz_question import QuizQuestionFilters


@dataclass
class QuizQuestionFiltersSchema(BaseFiltersSchema[QuizQuestionFilters]):
    resource_item_id: UUID
    count: int | None = None
    entity_cls: type[QuizQuestionFilters] = QuizQuestionFilters

    def to_entity(self) -> QuizQuestionFilters:
        return QuizQuestionFilters(count=self.count, offset=self.offset, resource_item_id=self.resource_item_id)
