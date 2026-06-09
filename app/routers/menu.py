from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext

from database.managers import UserManager
from keyboards.main_menu_keyboard import main_menu_keyboard
from settings.config import bot

router = Router()


@router.message(Command("menu"))
async def main_menu_command(message: Message, i18n: I18nContext):
    if not message.from_user or not message.from_user.id:
        return

    user = await UserManager.get_one(str(message.from_user.id))
    user_role = user.role

    reply_keyboard = main_menu_keyboard(user_role, message.from_user.language_code)
    await message.answer(
        i18n.get("main-menu-text"),
        reply_markup=reply_keyboard,
    )


@router.callback_query(F.data == "menu")
async def main_menu(callback: CallbackQuery, i18n: I18nContext):
    if not callback.from_user or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    user = await UserManager.get_one(str(callback.from_user.id))
    user_role = user.role
    reply_keyboard = main_menu_keyboard(user_role, callback.from_user.language_code)

    await callback.message.answer(
        i18n.get("main-menu-text"),
        reply_markup=reply_keyboard,
    )
