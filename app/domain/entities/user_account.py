from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums import Role


class UserAccountEntity(BaseEntity):
    user_account_id: UUID
    user_telegram_id: str
    username: str | None

    role: Role


class UserAccountUpdateEntity(BaseEntity):
    user_telegram_id: str | None
    username: str | None

    role: Role | None
