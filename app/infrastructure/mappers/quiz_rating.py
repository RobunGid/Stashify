from uuid import UUID

from domain.entities.quiz_rating import QuizRatingEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.quiz_rating import QuizRatingModel


class QuizRatingMapper(BaseMapper[QuizRatingEntity, QuizRatingModel]):
    def to_entity(self, model: QuizRatingModel) -> QuizRatingEntity:
        return QuizRatingEntity(
            quiz_rating_id=UUID(model.quiz_rating_id),
            quiz_item_id=UUID(model.quiz_item_id),
            user_account_id=UUID(model.user_account_id),
            rating=model.rating,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: QuizRatingEntity) -> QuizRatingModel:
        return QuizRatingModel(
            quiz_rating_id=entity.quiz_rating_id,
            quiz_item_id=entity.quiz_item_id,
            user_account_id=entity.user_account_id,
            rating=entity.rating,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
