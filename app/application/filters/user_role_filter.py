from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from application.services.user_account import UserAccountService
from dishka import FromDishka
from domain.enums import Role


class UserRoleFilter(BaseFilter):
    def __init__(
        self,
        roles: List[Role],
    ):
        self.roles = roles

    async def __call__(self, message: Message, service: FromDishka[UserAccountService]) -> bool:
        if not message.from_user or not message.from_user.id:
            return False
        user = await service.get_one_by_telegram_id(message.from_user.id)
        user_role = user.role if user else Role.user
        return user_role in self.roles
