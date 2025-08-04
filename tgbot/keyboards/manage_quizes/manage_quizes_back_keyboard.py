from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database.models.user import Role
from i18n.translate import t

def manage_quizes_back_keyboard(user_lang: Optional[str]):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_quizes"))

    return builder.as_markup()