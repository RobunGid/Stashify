from uuid import UUID

from domain.entities.quiz_result import QuizResultEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.quiz_result import QuizResultModel


class QuizResultMapper(BaseMapper[QuizResultEntity, QuizResultModel]):
    def to_entity(self, model: QuizResultModel) -> QuizResultEntity:
        return QuizResultEntity(
            quiz_result_id=UUID(model.quiz_result_id),
            quiz_item_id=UUID(model.quiz_item_id),
            user_account_id=UUID(model.user_account_id),
            percent=model.percent,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: QuizResultEntity) -> QuizResultModel:
        return QuizResultModel(
            quiz_result_id=entity.quiz_result_id,
            quiz_item_id=entity.quiz_item_id,
            user_account_id=entity.user_account_id,
            percent=entity.percent,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
