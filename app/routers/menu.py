from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext

from database.managers import UserManager
from routers.constants import ROLE_MENU_KEYBOARD_BUILDER_MAP
from settings.config import bot

router = Router()


@router.message(Command("menu"))
async def main_menu_command(message: Message, i18n: I18nContext):
    if not message.from_user or not message.from_user.id:
        return

    existing_user = await UserManager.get_one(str(message.from_user.id))
    existing_user_role = existing_user.role

    KeyboardBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[existing_user_role]
    keyboard_builder = KeyboardBuilder(i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        i18n.get("main-menu-text"),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "menu")
async def main_menu(callback: CallbackQuery, i18n: I18nContext):
    if not callback.from_user or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    existing_user = await UserManager.get_one(str(callback.from_user.id))
    existing_user_role = existing_user.role

    KeyboardBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[existing_user_role]
    keyboard_builder = KeyboardBuilder(i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        i18n.get("main-menu-text"),
        reply_markup=keyboard,
    )
