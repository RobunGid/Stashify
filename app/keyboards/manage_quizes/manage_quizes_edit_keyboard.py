from typing import Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t

class EditQuizActionCallbackFactory(CallbackData, prefix="edit_quiz_actn"):
    action: Union[Literal["edit"], Literal["delete"], Literal["add"]]
    resource_id: UUID4 | None

def manage_quizes_edit_keyboard(user_lang: str | None, resource_id: UUID4 | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.button(text=t("manage_quizes_keyboard.delete_question", user_lang), 
                                     callback_data=EditQuizActionCallbackFactory(action="delete", resource_id=resource_id))
    builder.button(text=t("manage_quizes_keyboard.edit_question", user_lang), 
                                     callback_data=EditQuizActionCallbackFactory(action="edit", resource_id=resource_id))
    builder.button(text=t("manage_quizes_keyboard.add_question", user_lang), 
                                     callback_data=EditQuizActionCallbackFactory(action="add", resource_id=resource_id))
    builder.button(text=t("common.back", user_lang), callback_data="menu")
    builder.adjust(1, 1, 1, 1)

    return builder.as_markup()