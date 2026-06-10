from aiogram.utils.keyboard import InlineKeyboardBuilder

from pydantic import UUID

from i18n import t
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory


def list_resources_quiz_final_keyboard(
    resource_item_id: UUID,
    page: int,
    user_lang: str = "en",
):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=t("start_quiz.retry", user_lang),
        callback_data=ListResourcesItemCallbackFactory(
            action="start_quiz",
            resource_item_id=resource_item_id,
            rating=0,
        ),
    )
    builder.button(
        text=t("common.back", user_lang),
        callback_data=ListResourcesChooseResourceCallbackFactory(
            action="change_page",
            page=page,
            resource_item_id=resource_item_id,
        ),
    )
    builder.adjust(1, 1)
    return builder.as_markup()
