from math import ceil

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.keyboards.menu import MenuBackKeyboardBuilder
from application.keyboards.search_resource import SearchResourceListKeyboardBuilder
from constants import FIND_RESOURCE_RESOURCES_ON_PAGE

from database.managers import ResourceManager
from settings.aiogram import bot

router = Router()


class SearchResourceState(StatesGroup):
    text = State()
    total_pages = State()
    resources = State()


@router.callback_query(F.data == "search_resource")
async def search_resource_start(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = MenuBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(text=i18n.get("search-resource-enter-text"), reply_markup=keyboard)
    await state.set_state(SearchResourceState.text)


@router.message(SearchResourceState.text)
async def search_resource_search(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code or not message:
        return

    resources = await ResourceManager.get_many(text=message.text)
    total_pages = ceil(len(resources) / FIND_RESOURCE_RESOURCES_ON_PAGE)
    await state.update_data(total_pages=total_pages, resources=resources)

    keyboard_builder = SearchResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await message.answer(text=i18n.get("search-resource-select"), reply_markup=keyboard)
