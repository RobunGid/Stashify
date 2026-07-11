from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject


class DeleteOldMessagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event,
        data: Dict[str, Any],
    ):
        state: FSMContext = data["state"]
        bot = data["bot"]
        if isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id if event.message else None
        if isinstance(event, Message):
            chat_id = event.chat.id

        state_data = await state.get_data()
        message_ids_to_delete = state_data.get("message_ids_to_delete", [])
        for message_id in message_ids_to_delete:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except TelegramAPIError:
                pass

        return await handler(event, data)
