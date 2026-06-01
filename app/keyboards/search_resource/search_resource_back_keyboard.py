from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database.models.user import Role
from i18n.translate import t

def search_resource_back_keyboard(user_lang: str = "en"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))

    return builder.as_markup()