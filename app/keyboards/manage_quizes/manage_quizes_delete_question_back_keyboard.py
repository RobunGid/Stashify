from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from i18n.translate import t


def manage_quizes_delete_question_back_keyboard(user_lang: str | None = "en"):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=t("common.back", user_lang),
            callback_data="manage_quizes",
        ),
    )

    return builder.as_markup()
