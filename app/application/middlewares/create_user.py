from aiogram import BaseMiddleware
from dishka import FromDishka

from application.schemas.user_account_schema import UserAccountSchema
from application.services.user_account import UserAccountService


class CreateUserMiddleware(BaseMiddleware):
    def __init__(self, user_account_service: FromDishka[UserAccountService]):
        self.user_service = user_account_service

    async def __call__(self, handler, event, data):
        user = event.from_user
        if user is None:
            return await handler(event, data)

        account = await self.user_service.get_one_by_telegram_id(user.id)

        if account is None:
            user_account_schema = UserAccountSchema(username=user.username, telegram_id=user.id)

            await self.user_service.create(item=user_account_schema.to_entity())

        data["db_user"] = account

        return await handler(event, data)
