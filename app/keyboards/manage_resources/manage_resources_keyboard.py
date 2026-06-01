from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def manage_resources_keyboard(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_resources_keyboard.create", user_lang), callback_data="create_resource"))
    builder.row(InlineKeyboardButton(text=t("manage_resources_keyboard.edit", user_lang), callback_data="edit_resource"))
    builder.row(InlineKeyboardButton(text=t("manage_resources_keyboard.delete", user_lang), callback_data="delete_resource"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()