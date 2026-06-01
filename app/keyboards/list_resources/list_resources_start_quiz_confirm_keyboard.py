from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import UUID4

from i18n.translate import t
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory

def list_resources_start_quiz_confirm_keyboard(resource_id: UUID4, user_lang: str = "en", page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.button(text=t("list_resources.start_quiz.confirm", user_lang), callback_data=ListResourcesItemCallbackFactory(action="start_quiz_cnfrm", resource_id=resource_id, rating=0))
    builder.button(text=t("common.back", user_lang), callback_data=ListResourcesChooseResourceCallbackFactory(action="change_page", page=page, resource_id=resource_id))

    return builder.as_markup()