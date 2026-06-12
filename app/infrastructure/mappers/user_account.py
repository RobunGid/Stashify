from uuid import UUID

from domain.entities.user_account import UserAccountEntity
from domain.enums import Role
from infrastructure.mappers.base import BaseMapper
from infrastructure.models.user_account import UserAccountModel


class UserAccountMapper(BaseMapper[UserAccountEntity, UserAccountModel]):
    def to_entity(self, model: UserAccountModel) -> UserAccountEntity:
        return UserAccountEntity(
            user_account_id=UUID(model.user_account_id),
            user_telegram_id=model.user_telegram_id,
            username=model.username,
            role=Role(model.role),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: UserAccountEntity) -> UserAccountModel:
        return UserAccountModel(
            user_account_id=str(entity.user_account_id),
            user_telegram_id=entity.user_telegram_id,
            username=entity.username,
            role=entity.role,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
