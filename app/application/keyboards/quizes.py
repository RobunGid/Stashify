from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BaseBackKeyboardBuilder,
    BaseConfirmKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
)
from application.schemas.category_item_schema import CategoryItemSchema
from application.schemas.resource_schema import ResourceItemSchema


class EditQuizActionCallbackFactory(CallbackData, prefix="edit_quiz_actn"):  # type: ignore[call-arg]
    action: Union[Literal["edit"], Literal["delete"], Literal["add"]]
    resource_item_id: UUID | None


@dataclass
class QuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-keyboard-add-question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="add",
                    resource_item_id=None,
                ),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-edit-question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="edit",
                    resource_item_id=None,
                ),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-delete-question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="delete",
                    resource_item_id=None,
                ),
            },
        ]

    def _back_callback(self) -> str:
        return "menu"


class EditQuizChooseResourceCallbackFactory(CallbackData, prefix="edit_quiz_rsc"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


class EditQuizResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema]):
    def _back_callback(self) -> str | CallbackData | None:
        return EditQuizChooseResourceCallbackFactory(
            action="change_page",
            resource_item_id=None,
            page=self.current_page - 1,
        )

    def _pagination_callback(self, page: int) -> CallbackData:
        return EditQuizChooseResourceCallbackFactory(action="change_page", resource_item_id=None, page=page)

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditQuizChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
            ),
        }


class EditQuizChooseCategoryCallbackFactory(CallbackData, prefix="edit_quiz_ctg"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


class EditQuizCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str | CallbackData | None:
        return EditQuizChooseCategoryCallbackFactory(
            action="change_page",
            category_id=None,
            page=self.current_page - 1,
        )

    def _pagination_callback(self, page: int) -> CallbackData:
        return EditQuizChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page)

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditQuizChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_item_id,
                page=0,
            ),
        }


@dataclass
class ManageQuizesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_quizes"


class DeleteQuizChooseResourceCallbackFactory(CallbackData, prefix="delete_quiz_rsc"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


class DeleteQuizResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema]):
    def _back_callback(self) -> str:
        return "manage_quizes"

    def _pagination_callback(self, page: int) -> CallbackData:
        return DeleteQuizChooseResourceCallbackFactory(action="change_page", resource_item_id=None, page=page)

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteQuizChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
            ),
        }


class DeleteQuizChooseCategoryCallbackFactory(CallbackData, prefix="delete_quiz_ctg"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


class DeleteQuizCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str:
        return "manage_quizes"

    def _pagination_callback(self, page: int) -> CallbackData:
        return DeleteQuizChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page)

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteQuizChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_item - id,
                page=0,
            ),
        }


class CreateQuizChooseCategoryCallbackFactory(CallbackData, prefix="create_quiz_ctg"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


class CreateQuizCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str:
        return "manage_quizes"

    def _pagination_callback(self, page: int) -> CallbackData:
        return CreateQuizChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page)

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": CreateQuizChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_item - id,
                page=0,
            ),
        }


class CreateQuizChooseResourceCallbackFactory(CallbackData, prefix="create_quiz_rsc"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


class CreateQuizResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema]):
    def _back_callback(self) -> str:
        return "manage_quizes"

    def _pagination_callback(self, page: int) -> CallbackData:
        return CreateQuizChooseResourceCallbackFactory(action="change_page", resource_item_id=None, page=page)

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": CreateQuizChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
            ),
        }


class DeleteQuizConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder):
    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-delete-confirm"),
                "callback_data": "delete_quiz_confirm",
            },
        ]

    def _back_callback(self) -> str:
        return "manage_quizes"


class QuizConfirmFinishKeyboardBuilder(BaseConfirmKeyboardBuilder):
    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-create-stop-questions"),
                "callback_data": "delete_quiz_confirm",
            },
        ]

    def _back_callback(self) -> str:
        return "manage_quizes"
