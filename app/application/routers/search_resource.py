from math import ceil

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.filters.valid_callback_filter import ValidCallbackFilter
from application.filters_schemas.resource_item import ResourceItemFiltersSchema
from application.keyboards.menu import MenuBackKeyboardBuilder
from application.keyboards.resources import ListSearchResourcesItemCallbackFactory, SearchResourceListKeyboardBuilder
from application.keyboards.search_resource import BackToSearchResourcesKeyboardBuilder
from application.routers.constants import SEARCH_RESOURCES_RESOURCES_ON_PAGE
from application.services.resource_item import ResourceItemService
from dishka import FromDishka

from settings.aiogram import bot

router = Router()
router.callback_query.filter(ValidCallbackFilter())


class SearchResourceState(StatesGroup):
    text = State()
    total_pages = State()
    resources = State()


@router.callback_query(F.data == "search_resource")
async def search_resource_item_start(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = MenuBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    answer_message = await callback.message.answer(text=i18n.get("search-resource-enter-text"), reply_markup=keyboard)
    await state.update_data(message_ids_to_delete=[answer_message.message_id])
    await state.set_state(SearchResourceState.text)


@router.message(SearchResourceState.text)
async def search_resource_item_search(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await state.update_data(query=message.text)
    filters = ResourceItemFiltersSchema(
        count=SEARCH_RESOURCES_RESOURCES_ON_PAGE,
        query=message.text,
    )
    resource_item_entities, count = await resource_item_service.get_many(filters.to_entity())
    total_resources_pages = ceil(count / SEARCH_RESOURCES_RESOURCES_ON_PAGE)

    if count == 0:
        keyboard_builder = BackToSearchResourcesKeyboardBuilder(
            i18n,
        )
        keyboard = keyboard_builder.build()

        await message.answer(
            text=i18n.get("list-search-resources-not-found", query=message.text),
            reply_markup=keyboard,
        )
    else:
        keyboard_builder = SearchResourceListKeyboardBuilder(
            i18n,
            items=resource_item_entities,
            current_page=0,
            total_pages=total_resources_pages,
            query=message.text or " ",
        )
        keyboard = keyboard_builder.build()

        await message.answer(
            text=i18n.get("list-search-resources-change-page", query=message.text),
            reply_markup=keyboard,
        )


@router.callback_query(
    ListSearchResourcesItemCallbackFactory.filter(),
)
async def search_resources_list_page(
    callback: CallbackQuery,
    callback_data: ListSearchResourcesItemCallbackFactory,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
    message: Message,
):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    current_page = callback_data.page
    query = callback_data.query

    filters = ResourceItemFiltersSchema(
        count=SEARCH_RESOURCES_RESOURCES_ON_PAGE,
        query=query,
        offset=current_page * SEARCH_RESOURCES_RESOURCES_ON_PAGE,
    )
    resource_item_entities, count = await resource_item_service.get_many(filters.to_entity())
    total_resources_pages = ceil(count / SEARCH_RESOURCES_RESOURCES_ON_PAGE)

    keyboard_builder = SearchResourceListKeyboardBuilder(
        i18n,
        items=resource_item_entities,
        current_page=current_page,
        total_pages=total_resources_pages,
        query=query,
    )
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "list-resources-change-page",
        ),
        reply_markup=keyboard,
    )
