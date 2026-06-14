from uuid import UUID

from domain.entities.quiz_question import QuizQuestionEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.quiz_question import QuizQuestionModel


class QuizQuestionMapper(BaseMapper[QuizQuestionEntity, QuizQuestionModel]):
    @staticmethod
    def to_entity(model: QuizQuestionModel) -> QuizQuestionEntity:
        return QuizQuestionEntity(
            quiz_question_id=UUID(str(model.quiz_question_id)),
            text=model.text,
            quiz_item_id=UUID(str(model.quiz_item_id)),
            options=model.options,
            right_options=model.right_options,
            image=model.image,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: QuizQuestionEntity) -> QuizQuestionModel:
        return QuizQuestionModel(
            quiz_question_id=str(entity.quiz_question_id),
            text=entity.text,
            quiz_item_id=str(entity.quiz_item_id),
            options=entity.options,
            right_options=entity.right_options,
            image=entity.image,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
