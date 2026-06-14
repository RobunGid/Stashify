from uuid import UUID

from domain.entities.quiz_item import QuizItemEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.quiz_item import QuizItemModel


class QuizItemMapper(BaseMapper[QuizItemEntity, QuizItemModel]):
    @staticmethod
    def to_entity(model: QuizItemModel) -> QuizItemEntity:
        return QuizItemEntity(
            quiz_item_id=UUID(str(model.quiz_item_id)),
            resource_item_id=UUID(str(model.resource_item_id)),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: QuizItemEntity) -> QuizItemModel:
        return QuizItemModel(
            quiz_item_id=str(entity.quiz_item_id),
            resource_item_id=str(entity.resource_item_id),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
