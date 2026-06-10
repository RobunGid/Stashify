from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from i18n.translate import t


class EditQuizActionCallbackFactory(CallbackData, prefix="edit_quiz_actn"):  # type: ignore[call-arg]
    action: Union[Literal["edit"], Literal["delete"], Literal["add"]]
    resource_item_id: UUID | None


def manage_quizes_edit_keyboard(user_lang: str | None, resource_item_id: UUID | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t("manage_quizes_keyboard.delete_question", user_lang),
        callback_data=EditQuizActionCallbackFactory(
            action="delete",
            resource_item_id=resource_item_id,
        ),
    )
    builder.button(
        text=t("manage_quizes_keyboard.edit_question", user_lang),
        callback_data=EditQuizActionCallbackFactory(
            action="edit",
            resource_item_id=resource_item_id,
        ),
    )
    builder.button(
        text=t("manage_quizes_keyboard.add_question", user_lang),
        callback_data=EditQuizActionCallbackFactory(
            action="add",
            resource_item_id=resource_item_id,
        ),
    )
    builder.button(text=t("common.back", user_lang), callback_data="menu")
    builder.adjust(1, 1, 1, 1)

    return builder.as_markup()
