from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from application.containers.factories import get_container
from application.services.user_account import UserAccountService
from domain.entities.user_account import Role


class UserRoleFilter(BaseFilter):
    def __init__(
        self,
        roles: List[Role],
    ):
        self.roles = roles

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        if not message.from_user or not message.from_user.id:
            return False
        container = get_container()
        async with container() as request_container:
            service = await request_container.get(UserAccountService)
            user = await service.get_one_by_telegram_id(message.from_user.id)
            user_role = user.role if user else Role.user
            return user_role in self.roles
