from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def manage_quizes_edit_keyboard(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.create", user_lang), callback_data="create_quiz"))
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.edit", user_lang), callback_data="edit_quiz"))
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.delete", user_lang), callback_data="delete_quiz"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()