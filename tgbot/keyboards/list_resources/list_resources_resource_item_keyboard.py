from typing import List, Literal, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema

class ListResourcesItemCallbackFactory(CallbackData, prefix="lst_rsc_itm"):
    action: Union[Literal["change_page"], Literal["add_favorite"], Literal["remove_favorite"], Literal["rate"], Literal["start_quiz"], Literal["start_quiz_cnfrm"]]
    resource_id: UUID4 | None
    rating: int | None

def list_resources_resource_item_keyboard(
        resources: List[ResourceSchema], 
        resource: ResourceSchema, 
        user_lang: str = "en", 
        is_favorite: bool = False, 
        rating: int = 0,
        has_quiz: bool = False,
        quiz_percent: int = 0
    ):
    builder = InlineKeyboardBuilder()
    resource_index = resources.index(resource)
    resource_quantity = len(resources)
    first_line_buttons_quantity = 1
    if resource_index+1 != resource_quantity and resource_index != 0:
            builder.button(text=t("items.start", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[0].id, rating=0))
            builder.button(text=t("items.back", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id, rating=0))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id, rating=0))
            builder.button(text=t("items.end", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[-1].id, rating=0))
            first_line_buttons_quantity = 5
    elif resource_index == 0 and resource_quantity != 1:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id, rating=0))
            builder.button(text=t("items.end", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[-1].id, rating=0))
            first_line_buttons_quantity = 3
    elif resource_index+1 == resource_quantity and resource_quantity != 1:
            builder.button(text=t("items.start", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[0].id, rating=0))
            builder.button(text=t("items.back", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id, rating=0))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            first_line_buttons_quantity = 3
    elif resource_index == 0 and resource_quantity == 0:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            first_line_buttons_quantity = 1
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="resources"))
  
    if not is_favorite:    
        builder.button(text=t("favorite.add", user_lang), callback_data=ListResourcesItemCallbackFactory(action="add_favorite", resource_id=resource.id, rating=0))
    if is_favorite:
        builder.button(text=t("favorite.remove", user_lang), callback_data=ListResourcesItemCallbackFactory(action="remove_favorite", resource_id=resource.id, rating=0))
    for i in range(1, 6):
        symbol = "⭐" if i <= rating else "☆"
        builder.button(text=symbol, callback_data=ListResourcesItemCallbackFactory(action="rate", resource_id=resource.id, rating=i))
    
    if quiz_percent != 0 and has_quiz:
        builder.button(text=t("start_quiz.completed", user_lang).format(percent=quiz_percent), callback_data=ListResourcesItemCallbackFactory(action="start_quiz", resource_id=resource.id, rating=0))
    if quiz_percent == 0 and has_quiz:
        builder.button(text=t("start_quiz.firstly", user_lang), callback_data=ListResourcesItemCallbackFactory(action="start_quiz", resource_id=resource.id, rating=0))

    builder.adjust(first_line_buttons_quantity, 2, 5)
    return builder.as_markup()

        
