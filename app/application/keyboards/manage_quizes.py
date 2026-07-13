from dataclasses import dataclass
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BaseBackKeyboardBuilder,
    BaseBackKeyboardBuilderMixin,
    BaseConfirmKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
)
from application.keyboards.resources import ListCategoriesItemCallbackFactory, ListCategoryResourcesItemCallbackFactory
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


@dataclass
class BackToManageQuizesKeyboardBuilderMixin(BaseBackKeyboardBuilderMixin):
    def _back_callback(self) -> str:
        return "manage_quizes"


@dataclass
class QuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-keyboard-create"),
                "callback_data": ListCategoriesItemCallbackFactory(action="change_page", context="crt_quiz", page=0),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-delete"),
                "callback_data": ListCategoriesItemCallbackFactory(action="change_page", context="dlt_quiz", page=0),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-create-question"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="crt_quiz_qstn",
                    page=0,
                ),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-edit-question"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="edt_quiz_qstn",
                    page=0,
                ),
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-delete-question"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="dlt_quiz_qstn",
                    page=0,
                ),
            },
        ]

    def _back_callback(self) -> str:
        return "menu"


class EditQuizQuestionChooseResourceCallbackFactory(CallbackData, prefix="edt_quiz_qstn_chs"):  # type: ignore[call-arg]
    resource_item_id: UUID | None


@dataclass
class EditQuizQuestionResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=self.current_page - 1,
            context="edt_quiz_qstn",
        ).pack()

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.category_item_id,
            page=page,
            context="edt_quiz_qst",
        ).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": EditQuizQuestionChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ),
        }


class CreateQuizQuestionChooseResourceCallbackFactory(
    CallbackData,
    prefix="crt_quiz_qstn_chs",  # type: ignore[call-arg]
):
    resource_item_id: UUID | None


@dataclass
class CreateQuizQuestionResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=self.current_page - 1,
            context="crt_quiz_qstn",
        ).pack()

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.category_item_id,
            page=page,
            context="crt_quiz_qst",
        ).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": CreateQuizQuestionChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ),
        }


class DeleteQuizQuestionChooseResourceCallbackFactory(
    CallbackData,
    prefix="crt_quiz_qstn_chs",  # type: ignore[call-arg]
):
    resource_item_id: UUID | None


@dataclass
class DeleteQuizQuestionResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=self.current_page - 1,
            context="dlt_quiz_qstn",
        ).pack()

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.category_item_id,
            page=page,
            context="dlt_quiz_qst",
        ).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteQuizQuestionChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ),
        }


@dataclass
class EditQuizQuestionCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToManageQuizesKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(action="change_page", page=page, context="edt_quiz_qstn").pack()

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="edt_quiz_qst",
            ).pack(),
        }


@dataclass
class BackToManageQuizesKeyboardBuilder(BaseBackKeyboardBuilder, BackToManageQuizesKeyboardBuilderMixin):
    pass


class DeleteQuizChooseResourceCallbackFactory(CallbackData, prefix="edt_quiz_qstn_chs"):  # type: ignore[call-arg]
    resource_item_id: UUID | None


@dataclass
class DeleteQuizResourceListKeyboardBuilder(
    BaseListKeyboardBuilder[ResourceItemEntity],
    BackToManageQuizesKeyboardBuilder,
):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.category_item_id,
            page=page,
            context="dlt_quiz",
        ).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteQuizChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ).pack(),
        }


@dataclass
class DeleteQuizCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToManageQuizesKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(action="change_page", page=page, context="dlt_quiz").pack()

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="dlt_quiz",
            ).pack(),
        }


@dataclass
class CreateQuizCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToManageQuizesKeyboardBuilder,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(page=page, action="change_page", context="crt_quiz").pack()

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="crt_quiz",
            ).pack(),
        }


class CreateQuizChooseResourceCallbackFactory(CallbackData, prefix="crt_quiz_chs"):  # type: ignore[call-arg]
    resource_item_id: UUID | None


@dataclass
class CreateQuizResourceListKeyboardBuilder(
    BaseListKeyboardBuilder[ResourceItemEntity],
    BackToManageQuizesKeyboardBuilder,
):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            page=page,
            category_item_id=self.category_item_id,
            context="crt_quiz",
        ).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": CreateQuizChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ).pack(),
        }


@dataclass
class DeleteQuizConfirmKeyboardBuilder(BackToManageQuizesKeyboardBuilderMixin, BaseConfirmKeyboardBuilder):
    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-delete-confirm"),
                "callback_data": "delete_quiz_confirm",
            },
        ]


@dataclass
class FinishQuizConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder, BackToManageQuizesKeyboardBuilderMixin):
    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-create-stop-questions"),
                "callback_data": "finish_quiz_confirm",
            },
        ]


@dataclass
class CreateQuizQuestionCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToManageQuizesKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(page=page, context="crt_quiz_qstn", action="change_page").pack()

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="crt_quiz_qst",
            ).pack(),
        }


@dataclass
class DeleteQuizQuestionCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToManageQuizesKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(page=page, context="dlt_quiz_qstn", action="change_page").pack()

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="dlt_quiz_qst",
            ).pack(),
        }
