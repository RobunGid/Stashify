from typing import Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t

def manage_quizes_delete_question_back_keyboard(user_lang: str | None = "en"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_quizes"))

    return builder.as_markup()