from uuid import UUID

from domain.entities.quiz_option import QuizOptionEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.quiz_option import QuizOptionModel


class QuizOptionMapper(BaseMapper[QuizOptionEntity, QuizOptionModel]):
    @staticmethod
    def to_entity(model: QuizOptionModel) -> QuizOptionEntity:
        return QuizOptionEntity(
            quiz_question_id=UUID(str(model.quiz_question_id)),
            text=model.text,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_right=model.is_right,
        )

    @staticmethod
    def to_model(entity: QuizOptionEntity) -> QuizOptionModel:
        return QuizOptionModel(
            quiz_question_id=str(entity.quiz_question_id),
            text=entity.text,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_right=entity.is_right,
        )
