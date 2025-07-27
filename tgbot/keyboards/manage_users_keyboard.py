from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def manage_users_keyboard(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_users_keyboard.edit", user_lang), callback_data="edit_user"))
    builder.row(InlineKeyboardButton(text=t("manage_users_keyboard.block", user_lang), callback_data="block_user"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()