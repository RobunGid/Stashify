from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from i18n.translate import t

def list_resources_start_quiz_confirm_keyboard(user_lang: str = "en"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("list_resources.start_quiz.confirm", user_lang), callback_data="start_quiz_confirm"))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()