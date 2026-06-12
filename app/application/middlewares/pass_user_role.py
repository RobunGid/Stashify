from aiogram import BaseMiddleware

from application.services.user_account import UserAccountService
from dishka import FromDishka
from domain.enums import Role


class PassUserRoleMiddleware(BaseMiddleware):
    def __init__(self, user_service: FromDishka[UserAccountService]):
        self.user_service = user_service

    async def __call__(self, handler, event, data):
        user = event.from_user
        if user is None:
            data["role"] = None
            return await handler(event, data)

        user_account = await self.user_service.get_one_by_telegram_id(user.id)
        role = user_account.role if user_account else Role.user

        data["role"] = role

        return await handler(event, data)
