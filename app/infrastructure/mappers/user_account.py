from uuid import UUID

from domain.entities.user_account import Role, UserAccountEntity
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.user_account import UserAccountModel


class UserAccountMapper(BaseMapper[UserAccountEntity, UserAccountModel]):
    @staticmethod
    def to_entity(model: UserAccountModel) -> UserAccountEntity:
        return UserAccountEntity(
            user_account_id=UUID(str(model.user_account_id)),
            user_telegram_id=model.user_telegram_id,
            username=model.username,
            role=Role(model.role),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: UserAccountEntity) -> UserAccountModel:
        return UserAccountModel(
            user_account_id=str(entity.user_account_id),
            user_telegram_id=entity.user_telegram_id,
            username=entity.username,
            role=entity.role,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
