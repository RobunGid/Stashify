from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.exceptions.user_account import UserAccountNotFoundException
from application.routers.constants import ROLE_MENU_KEYBOARD_BUILDER_MAP
from application.services.user_account import UserAccountService
from dishka import FromDishka

from settings.aiogram import bot

router = Router()


@router.message(Command("menu"))
async def main_menu_command_message_handler(
    message: Message,
    i18n: I18nContext,
    service: FromDishka[UserAccountService],
):
    if not message.from_user or not message.from_user.id:
        return

    existing_user = await service.get_one_by_telegram_id(message.from_user.id)

    if existing_user is None:
        raise UserAccountNotFoundException(identifier=message.from_user.id)

    existing_user_role = existing_user.role

    KeyboardBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[existing_user_role]
    keyboard_builder = KeyboardBuilder(i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        i18n.get("main-menu-text"),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "menu")
async def main_menu_callback_handler(
    callback: CallbackQuery,
    i18n: I18nContext,
    service: FromDishka[UserAccountService],
):
    if not callback.from_user or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    existing_user = await service.get_one_by_telegram_id(
        telegram_id=callback.message.chat.id,
    )

    if existing_user is None:
        raise UserAccountNotFoundException(identifier=callback.message.chat.id)

    existing_user_role = existing_user.role

    KeyboardBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[existing_user_role]
    keyboard_builder = KeyboardBuilder(i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        i18n.get("main-menu-text"),
        reply_markup=keyboard,
    )
