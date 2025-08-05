from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def manage_quizes_delete_keyboard_confirm(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_quizes.delete.confirm", user_lang), callback_data="delete_quiz_confirm"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_quizes"))

    return builder.as_markup()