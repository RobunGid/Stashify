# from math import ceil
# from typing import List
# from uuid import uuid4

from aiogram import Router

# from aiogram import F
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import CallbackQuery, Message, PhotoSize
# from aiogram.utils.media_group import MediaGroupBuilder

# from aiogram_i18n import I18nContext
# from aiogram_media_group import media_group_handler
# from application.filters.user_role_filter import UserRoleFilter
# from application.filters_schemas.category_item import CategoryItemFiltersSchema
# from application.filters_schemas.resource_item import ResourceItemFiltersSchema
# from application.keyboards.resources import (
#     CreateResourceCategoryListKeyboardBuilder,
#     DeleteResourceCategoryListKeyboardBuilder,
#     DeleteResourceConfirmKeyboardBuilder,
#     DeleteResourceResourceListKeyboardBuilder,
#     EditResourceCategoryListKeyboardBuilder,
#     EditResourceChooseFieldKeyboardBuilder,
#     EditResourceResourceListKeyboardBuilder,
#     ManageResourcesBackKeyboardBuilder,
#     ResourceManageEntryKeyboardBuilder,
# )
# from application.routers.constants import (
#     CREATE_RESOURCE_CATEGORIES_ON_PAGE,
#     DELETE_RESOURCE_CATEGORIES_ON_PAGE,
#     DELETE_RESOURCE_RESOURCES_ON_PAGE,
#     EDIT_RESOURCE_CATEGORIES_ON_PAGE,
#     EDIT_RESOURCE_RESOURCES_ON_PAGE,
# )
# from application.schemas.resource_image_schema import BsaeResourceImageSchema
# from application.schemas.resource_schema import BaseResourceItemSchema, ResourceItemSchema
# from application.services.category_item import CategoryItemService
# from application.services.resource_image import ResourceImageService
# from application.services.resource_item import ResourceItemService
# from dishka import FromDishka
# from infrastructure.models.user_account import Role
# from sqlalchemy.exc import IntegrityError

# from settings.aiogram import bot

router = Router()


# @router.callback_query(
#     F.data == "manage_resources",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def manage_resources(callback: CallbackQuery, i18n: I18nContext):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message:
#         return
#     keyboard_builder = ResourceManageEntryKeyboardBuilder(i18n)
#     keyboard = keyboard_builder.build()
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-text",
#         ),
#         reply_markup=keyboard,
#     )


# class CreateResourceState(StatesGroup):
#     total_pages = State()
#     categories = State()
#     category_item_id = State()
#     name = State()
#     description = State()
#     links = State()
#     images = State()
#     tags = State()


# @router.callback_query(
#     F.data == "create_resource",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def create_resource_callback_handler(
#     callback: CallbackQuery,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[CategoryItemService],
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )

#     filters = CategoryItemFiltersSchema(count=CREATE_RESOURCE_CATEGORIES_ON_PAGE)
#     categories, count = await service.get_many(filters.to_entity())
#     total_pages = ceil(count / CREATE_RESOURCE_CATEGORIES_ON_PAGE)
#     await state.update_data(total_pages=total_pages, categories=categories)

#     keyboard_builder = CreateResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=categories,
#         current_page=1,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-create-choose-category",
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state("resource_item_id")


# @router.callback_query(
#     CreateResourceCallbackFactory.filter(F.action == "change_page"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def create_resource_page(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: CreateResourceCallbackFactory,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     current_page = callback_data.page

#     await state.update_data(current_page=current_page)

#     categories_data = await state.get_data()
#     categories = categories_data["categories"][
#         (current_page - 1) * CREATE_RESOURCE_CATEGORIES_ON_PAGE : current_page * (CREATE_RESOURCE_CATEGORIES_ON_PAGE)
#     ]
#     total_pages = categories_data["total_pages"]

#     keyboard_builder = CreateResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=categories,
#         current_page=current_page,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-create-choose-category",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     CreateResourceCallbackFactory.filter(F.action == "select"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def create_resource_choose(
#     callback: CallbackQuery,
#     callback_data: CreateResourceCallbackFactory,
#     state: FSMContext,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-create-wait-name",
#         ),
#         reply_markup=keyboard,
#     )

#     await state.update_data(category_item_id=callback_data.category_item_id)
#     await state.set_state(CreateResourceState.name)


# @router.message(
#     CreateResourceState.name,
#     F.text,
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def new_resource_name_choose(message: Message, state: FSMContext, i18n: I18nContext):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     await state.update_data(name=message.html_text)

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await message.answer(
#         text=i18n.get(
#             "manage-resources-create-wait-description",
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state(CreateResourceState.description)


# @router.message(
#     CreateResourceState.description,
#     F.text,
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def new_resource_description_choose(message: Message, state: FSMContext, i18n: I18nContext):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     await state.update_data(description=message.html_text)

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await message.answer(
#         text=i18n.get(
#             "manage-resources-create-wait-links",
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state(CreateResourceState.links)


# @router.message(
#     CreateResourceState.links,
#     F.text,
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def new_resource_links_choose(message: Message, state: FSMContext, i18n: I18nContext):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     await state.update_data(links=message.html_text)

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await message.answer(
#         text=i18n.get(
#             "manage-resources-create-wait-images",
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state(CreateResourceState.images)


# @router.message(F.media_group_id, CreateResourceState.images)
# @media_group_handler
# async def new_resource_image_choose(messages: List[Message], state: FSMContext, i18n: I18nContext):
#     if not messages[0].from_user or not messages[0].from_user.language_code:
#         return
#     await state.update_data(images=[message.photo[-1].file_id for message in messages if message.photo])

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await messages[0].answer(
#         text=i18n.get(
#             "manage-resources-create-wait-tags",
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state(CreateResourceState.tags)


# @router.message(CreateResourceState.tags, F.text)
# async def new_resource_tags_choose(
#     message: Message,
#     state: FSMContext,
#     i18n: I18nContext,
#     resource_item_service: FromDishka[ResourceItemService],
#     resource_image_service: FromDishka[ResourceImageService],
# ):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     state_data = await state.get_data()
#     resource_data = BaseResourceItemSchema(
#         category_item_id=state_data["category_item_id"],
#         resource_item_id=uuid4(),
#         name=state_data["name"],
#         description=state_data["description"],
#         links=state_data["links"],
#         tags=message.html_text,
#         verified=False,
#     )
#     category_name = next(
#         (category.name for category in state_data["categories"]),
#         "Unknown",
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         await resource_item_service.create(resource_data.to_entity())
#         for resource_image in state_data["images"]:
#             image = BsaeResourceImageSchema(
#                 resource_image_id=uuid4(),
#                 resource_item_id=resource_data.resource_item_id,
#                 image=resource_image,
#             )
#             await resource_image_service.create(image.to_entity())
#     except IntegrityError:
#         await message.answer(
#             text=i18n.get(
#                 "manage-resources-create-fail",
#                 resource_name=resource_data.name,
#                 resource_description=resource_data.description,
#                 resource_tags=resource_data.tags,
#                 category_name=category_name,
#             ),
#             reply_markup=keyboard,
#         )
#     else:
#         if len(state_data["images"]) > 1:
#             media_group = MediaGroupBuilder(
#                 caption=i18n.get(
#                     "manage-resources-create-success",
#                     resource_name=resource_data.name,
#                     resource_description=resource_data.description,
#                     resource_tags=resource_data.tags,
#                     category_name=category_name,
#                 ),
#             )
#             for image in state_data["images"]:
#                 media_group.add_photo(type="photo", media=image)
#             await message.answer_media_group(media=list(media_group.build()), reply_markup=keyboard)
#         else:
#             await message.answer_photo(
#                 photo=state_data["images"][0],
#                 caption=i18n.get(
#                     "manage-resources-create-success",
#                     resource_name=resource_data.name,
#                     resource_description=resource_data.description,
#                     resource_tags=resource_data.tags,
#                     category_name=category_name,
#                 ),
#                 reply_markup=keyboard,
#             )


# class DeleteResourceState(StatesGroup):
#     total_pages = State()
#     resources = State()
#     categories = State()
#     resource_item_id = State()
#     confirm = State()


# @router.callback_query(
#     F.data == "delete_resource",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_callback_handler(
#     callback: CallbackQuery,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[CategoryItemService],
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )

#     filters = CategoryItemFiltersSchema(count=DELETE_RESOURCE_CATEGORIES_ON_PAGE)
#     category_entities, count = await service.get_many(filters.to_entity())
#     total_pages = ceil(count / DELETE_RESOURCE_CATEGORIES_ON_PAGE)
#     await state.update_data(total_pages=total_pages, category_items=category_entities)

#     keyboard_builder = DeleteResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=category_entities,
#         total_pages=total_pages,
#         current_page=1,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-delete-choose-category",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     DeleteResourceChooseCategoryCallbackFactory.filter(F.action == "change_page"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_categories_page(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: DeleteResourceChooseCategoryCallbackFactory,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     current_page = callback_data.page

#     resources_data = await state.get_data()
#     categories = resources_data["categories"][
#         (current_page - 1) * DELETE_RESOURCE_CATEGORIES_ON_PAGE : current_page * (DELETE_RESOURCE_CATEGORIES_ON_PAGE)
#     ]
#     total_pages = resources_data["total_pages"]

#     keyboard_builder = DeleteResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=categories,
#         total_pages=total_pages,
#         current_page=current_page,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-delete-choose-category",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     DeleteResourceChooseCategoryCallbackFactory.filter(F.action == "select"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_category_select(
#     callback: CallbackQuery,
#     callback_data: DeleteResourceChooseCategoryCallbackFactory,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if (
#         not callback_data.category_item_id
#         or not callback.from_user
#         or not callback.from_user.language_code
#         or not callback.message
#         or not callback.data
#     ):
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )

#     current_page = callback_data.page
#     resources_data = await state.get_data()
#     category_item_id = callback_data.category_item_id
#     filters = ResourceItemFiltersSchema(category_item_id=category_item_id, count=DELETE_RESOURCE_CATEGORIES_ON_PAGE)
#     resources, count = await service.get_many(filters.to_entity())
#     total_pages = resources_data["total_pages"]
#     await state.update_data(category_item_id=category_item_id, resources=resources)

#     keyboard_builder = DeleteResourceResourceListKeyboardBuilder(
#         i18n=i18n,
#         items=resources,
#         current_page=current_page,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-delete-choose-resource",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     DeleteResourceChooseResourceCallbackFactory.filter(F.action == "change_page"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_page(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: DeleteResourceChooseResourceCallbackFactory,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     current_page = callback_data.page

#     resources_data = await state.get_data()
#     resources = resources_data["resources"][
#         (current_page - 1) * DELETE_RESOURCE_RESOURCES_ON_PAGE : current_page * (DELETE_RESOURCE_RESOURCES_ON_PAGE)
#     ]
#     total_pages = resources_data["total_pages"]

#     keyboard_builder = DeleteResourceResourceListKeyboardBuilder(
#         i18n=i18n,
#         items=resources,
#         current_page=current_page,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-delete-choose-resource",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     DeleteResourceChooseResourceCallbackFactory.filter(F.action == "select"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_select(
#     callback: CallbackQuery,
#     callback_data: DeleteResourceChooseResourceCallbackFactory,
#     state: FSMContext,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     resource_item_id = callback_data.resource_item_id
#     state_data = await state.get_data()
#     resource_item: ResourceItemSchema = next(
#         (resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id),
#     )

#     keyboard_builder = DeleteResourceConfirmKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await state.update_data(resource_item_id=resource_item_id)
#     await callback.message.answer(
#         text=i18n.get("manage-resources-delete-choose-to-delete", name=resource_item.name),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     F.data == "delete_resource_confirm",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def delete_resource_name_confirm(
#     callback: CallbackQuery,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     resource_data = await state.get_data()
#     resource: ResourceItemSchema = next(
#         (
#             resource
#             for resource in resource_data["resources"]
#             if resource.resource_item_id == resource_data["resource_item_id"]
#         ),
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         await service.delete_by_id(item_id=resource_data["resource_item_id"])
#     except IntegrityError, ValueError:
#         await callback.message.answer(
#             text=i18n.get("manage-resources-delete-fail", name=resource.name),
#             reply_markup=keyboard,
#         )
#     else:
#         await callback.message.answer(
#             text=i18n.get("manage-resources-delete-success", name=resource.name),
#             reply_markup=keyboard,
#         )


# class EditResourceState(StatesGroup):
#     total_pages = State()
#     resources = State()
#     categories = State()
#     resource_item_id = State()
#     name = State()
#     description = State()
#     image = State()
#     tags = State()


# @router.callback_query(
#     F.data == "edit_resource",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_callback_handler(
#     callback: CallbackQuery,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[CategoryItemService],
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )

#     filters = CategoryItemFiltersSchema(count=EDIT_RESOURCE_CATEGORIES_ON_PAGE)
#     category_entities, count = await service.get_many(filters.to_entity())
#     total_pages = ceil(count / EDIT_RESOURCE_CATEGORIES_ON_PAGE)
#     await state.update_data(total_pages=total_pages, category_items=category_entities)

#     keyboard_builder = EditResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=category_entities,
#         current_page=1,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-choose-category",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     EditResourceChooseCategoryCallbackFactory.filter(F.action == "change_page"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_category_page(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: EditResourceChooseCategoryCallbackFactory,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     current_page = callback_data.page

#     await state.update_data(current_page=current_page)

#     state_data = await state.get_data()
#     categories = state_data["categories"][
#         (current_page - 1) * EDIT_RESOURCE_CATEGORIES_ON_PAGE : current_page * (EDIT_RESOURCE_CATEGORIES_ON_PAGE)
#     ]
#     total_pages = state_data["total_pages"]

#     keyboard_builder = EditResourceCategoryListKeyboardBuilder(
#         i18n=i18n,
#         items=categories,
#         current_page=current_page,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-choose-category",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     EditResourceChooseCategoryCallbackFactory.filter(F.action == "select"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_category_choose(
#     callback: CallbackQuery,
#     callback_data: EditResourceChooseCategoryCallbackFactory,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if (
#         not callback_data.category_item_id
#         or not callback.from_user
#         or not callback.from_user.language_code
#         or not callback.message
#         or not callback.data
#     ):
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     category_item_id = callback_data.category_item_id
#     filters = ResourceItemFiltersSchema(category_item_id=category_item_id, count=EDIT_RESOURCE_RESOURCES_ON_PAGE)
#     resources, count = await service.get_many(filters.to_entity())
#     await state.update_data(resources=resources)
#     total_pages = ceil(count / EDIT_RESOURCE_RESOURCES_ON_PAGE)

#     keyboard_builder = EditResourceResourceListKeyboardBuilder(
#         i18n=i18n,
#         items=resources,
#         current_page=1,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await state.update_data(category_item_id=category_item_id)
#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-choose-to-change",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     EditResourceChooseResourceCallbackFactory.filter(F.action == "change_page"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_page(
#     callback: CallbackQuery,
#     state: FSMContext,
#     callback_data: EditResourceChooseResourceCallbackFactory,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     current_page = callback_data.page

#     await state.update_data(current_page=current_page)

#     resources_data = await state.get_data()
#     resources = resources_data["resources"][
#         (current_page - 1) * EDIT_RESOURCE_RESOURCES_ON_PAGE : current_page * (EDIT_RESOURCE_RESOURCES_ON_PAGE)
#     ]
#     total_pages = resources_data["total_pages"]

#     keyboard_builder = EditResourceResourceListKeyboardBuilder(
#         i18n=i18n,
#         items=resources,
#         current_page=current_page,
#         total_pages=total_pages,
#     )
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-choose",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     EditResourceChooseResourceCallbackFactory.filter(F.action == "select"),
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_choose(
#     callback: CallbackQuery,
#     callback_data: EditResourceChooseResourceCallbackFactory,
#     state: FSMContext,
#     i18n: I18nContext,
# ):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     resource_item_id = callback_data.resource_item_id
#     await state.update_data(resource_item_id=resource_item_id)

#     keyboard_builder = EditResourceChooseFieldKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-choose-to-change",
#         ),
#         reply_markup=keyboard,
#     )


# @router.callback_query(
#     F.data == "edit_resource_name",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_name(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     state_data = await state.get_data()
#     resource_name = next(
#         (
#             resource.name
#             for resource in state_data["resources"]
#             if resource.resource_item_id == state_data["resource_item_id"]
#         ),
#         "Unknown",
#     )

#     keyboard_builder = EditResourceChooseFieldKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get("manage-resources-edit-name-text", name=resource_name),
#         reply_markup=keyboard,
#     )
#     await state.set_state(EditResourceState.name)


# @router.message(
#     EditResourceState.name,
#     UserRoleFilter([Role.admin, Role.manager]),
#     F.text,
# )
# async def edit_resource_name_success(
#     message: Message,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if not message.from_user or not message.from_user.language_code:
#         return

#     resource_item_data = await state.get_data()

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         resource_item_data["name"] = message.html_text
#         await service.update(**resource_item_data)
#     except IntegrityError, ValueError:
#         await message.answer(
#             text=i18n.get("manage-resources-edit-name-fail", name=message.html_text),
#             reply_markup=keyboard,
#         )
#         await state.set_state(EditResourceState.name)
#     else:
#         await message.answer(
#             text=i18n.get("manage-resources-edit-name-success", name=message.html_text),
#             reply_markup=keyboard,
#         )


# @router.callback_query(
#     F.data == "edit_resource_description",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_description(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     state_data = await state.get_data()
#     resource_description = next(
#         (
#             resource.description
#             for resource in state_data["resources"]
#             if resource.resource_item_id == state_data["resource_item_id"]
#         ),
#         "Unknown",
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get("manage-resources-edit-description-text", description=resource_description),
#         reply_markup=keyboard,
#     )
#     await state.set_state(EditResourceState.description)


# @router.message(
#     EditResourceState.description,
#     UserRoleFilter([Role.admin, Role.manager]),
#     F.text,
# )
# async def edit_resource_description_success(
#     message: Message,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     resource_data = await state.get_data()

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         resource_data["description"] = message.html_text
#         await service.update(**resource_data)
#     except IntegrityError, ValueError:
#         await message.answer(
#             text=i18n.get("manage-resources-edit-description-fail", description=message.html_text),
#             reply_markup=keyboard,
#         )
#         await state.set_state(EditResourceState.description)
#     else:
#         await message.answer(
#             text=i18n.get("manage-resources-edit-description-success", description=message.html_text),
#             reply_markup=keyboard,
#         )


# @router.callback_query(
#     F.data == "edit_resource_tags",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_tags(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     state_data = await state.get_data()
#     resource_tags = next(
#         (
#             resource.tags
#             for resource in state_data["resources"]
#             if resource.resource_item_id == state_data["resource_item_id"]
#         ),
#         "Unknown",
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer(
#         text=i18n.get(
#             "manage-resources-edit-tags-text",
#             tags=resource_tags,
#         ),
#         reply_markup=keyboard,
#     )
#     await state.set_state(EditResourceState.tags)


# @router.message(
#     EditResourceState.tags,
#     UserRoleFilter([Role.admin, Role.manager]),
#     F.text,
# )
# async def edit_resource_tags_success(
#     message: Message,
#     state: FSMContext,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     resource_data = await state.get_data()
#     resource_data["tags"] = message.html_text

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         await service.update(**resource_data)
#     except IntegrityError, ValueError:
#         await message.answer(
#             text=i18n.get(
#                 "manage-resources-edit-tags-fail",
#                 tags=message.html_text,
#             ),
#             reply_markup=keyboard,
#         )
#         await state.set_state(EditResourceState.tags)
#     else:
#         await message.answer(
#             text=i18n.get(
#                 "manage-resources-edit-tags-success",
#                 tags=message.html_text,
#             ),
#             reply_markup=keyboard,
#         )


# @router.callback_query(
#     F.data == "edit_resource_image",
#     UserRoleFilter([Role.admin, Role.manager]),
# )
# async def edit_resource_image(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
#     if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
#         return
#     await bot.delete_message(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#     )
#     state_data = await state.get_data()
#     resource_image = next(
#         (
#             resource.image
#             for resource in state_data["resources"]
#             if resource.resource_item_id == state_data["resource_item_id"]
#         ),
#         "Unknown",
#     )

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     await callback.message.answer_photo(
#         photo=resource_image,
#         caption=i18n.get("manage-resources-edit-image-text"),
#         reply_markup=keyboard,
#     )
#     await state.set_state(EditResourceState.image)


# @router.message(
#     EditResourceState.image,
#     UserRoleFilter([Role.admin, Role.manager]),
#     F.photo[-1].as_("resource_image"),
# )
# async def edit_resource_image_success(
#     message: Message,
#     state: FSMContext,
#     resource_image: PhotoSize,
#     i18n: I18nContext,
#     service: FromDishka[ResourceItemService],
# ):
#     if not message.from_user or not message.from_user.language_code:
#         return
#     resource_data = await state.get_data()
#     resource_data["image"] = resource_image.file_id

#     keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
#     keyboard = keyboard_builder.build()

#     try:
#         await service.update(**resource_data)
#     except IntegrityError, ValueError:
#         await message.answer_photo(
#             photo=resource_image.file_id,
#             caption=i18n.get(
#                 "manage-resources-edit-image-fail",
#             ),
#             reply_markup=keyboard,
#         )
#         await state.set_state(EditResourceState.image)
#     else:
#         await message.answer_photo(
#             photo=resource_image.file_id,
#             caption=i18n.get(
#                 "manage-resources-edit-image-success",
#             ),
#             reply_markup=keyboard,
#         )
