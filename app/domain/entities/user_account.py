from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from domain.entities.base import BaseEntity, BaseUpdateEntity


@dataclass
class UserAccountEntity(BaseEntity):
    user_account_id: UUID
    user_telegram_id: int
    username: str | None

    role: Role


@dataclass
class UserAccountUpdateEntity(BaseUpdateEntity):
    user_telegram_id: int | None
    username: str | None

    role: Role | None


class Role(Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
