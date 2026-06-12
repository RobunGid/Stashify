from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from application.schemas.user_account_schema import UserAccountSchema
from application.services.user_account import UserAccountService
from dishka import AsyncContainer


class CreateUserMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer):
        self.container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        user = event.from_user
        if user is None:
            return await handler(event, data)
        async with self.container() as request_container:
            user_account_service = await request_container.get(UserAccountService)

            user_account = await user_account_service.get_one_by_telegram_id(user.id)

            if user_account is None:
                user_account_schema = UserAccountSchema(username=user.username, user_telegram_id=user.id)

                await user_account_service.create(item=user_account_schema.to_entity())

                user_account = await user_account_service.get_one_by_telegram_id(user.id)

            data["user"] = user_account

            return await handler(event, data)
