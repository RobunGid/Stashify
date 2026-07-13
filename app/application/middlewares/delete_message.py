import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ChatIdUnion, Message, TelegramObject


async def delete_message(message_id: int, bot: Bot, chat_id: ChatIdUnion):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramAPIError:
        pass


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
            if event.data == " ":
                return
        if isinstance(event, Message):
            chat_id = event.chat.id

        if not chat_id:
            return await handler(event, data)

        state_data = await state.get_data()
        message_ids_to_delete = state_data.get("message_ids_to_delete", [])
        await asyncio.gather(*(delete_message(message_id, bot, chat_id) for message_id in message_ids_to_delete))

        return await handler(event, data)
