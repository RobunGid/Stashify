from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def manage_quizes_edit_keyboard(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.delete_question", user_lang), callback_data="delete_question"))
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.edit_question", user_lang), callback_data="edit_question"))
    builder.row(InlineKeyboardButton(text=t("manage_quizes_keyboard.add_question", user_lang), callback_data="add_question"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()