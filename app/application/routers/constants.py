from typing import TypedDict

from application.keyboards.categories import DeleteCategoryListKeyboardBuilder, EditCategoryListKeyboardBuilder
from application.keyboards.manage_quizes import (
    CreateQuizCategoryListKeyboardBuilder,
    CreateQuizQuestionCategoryListKeyboardBuilder,
    CreateQuizQuestionResourceListKeyboardBuilder,
    CreateQuizResourceListKeyboardBuilder,
    DeleteQuizCategoryListKeyboardBuilder,
    DeleteQuizQuestionCategoryListKeyboardBuilder,
    DeleteQuizQuestionResourceListKeyboardBuilder,
    DeleteQuizResourceListKeyboardBuilder,
    EditQuizQuestionCategoryListKeyboardBuilder,
    EditQuizQuestionResourceListKeyboardBuilder,
)
from application.keyboards.menu import (
    AdminMenuKeyboardBuilder,
    BaseMenuKeyboardBuilder,
    ManagerMenuKeyboardBuilder,
    UserMenuKeyboardBuilder,
)
from application.keyboards.resources import (
    CategoryListKeyboardBuilder,
    CategoryResourceListKeyboardBuilder,
    CreateResourceCategoryListKeyboardBuilder,
    DeleteResourceCategoryListKeyboardBuilder,
    DeleteResourceResourceListKeyboardBuilder,
    EditResourceCategoryListKeyboardBuilder,
    EditResourceResourceListKeyboardBuilder,
    ResourceItemKeyboardBuilder,
)
from application.keyboards.search_resource import SearchResourceItemKeyboardBuilder
from infrastructure.models.user_account import Role

ROLE_MENU_KEYBOARD_BUILDER_MAP: dict[Role, type[BaseMenuKeyboardBuilder]] = {
    Role.admin: AdminMenuKeyboardBuilder,
    Role.manager: ManagerMenuKeyboardBuilder,
    Role.user: UserMenuKeyboardBuilder,
}


class CategoryListKeyboardBuilerMapType(TypedDict):
    menu: type[CategoryListKeyboardBuilder]
    crt_rsc: type[CreateResourceCategoryListKeyboardBuilder]
    edt_rsc: type[EditResourceCategoryListKeyboardBuilder]
    dlt_rsc: type[DeleteResourceCategoryListKeyboardBuilder]
    edt_ctg: type[EditCategoryListKeyboardBuilder]
    dlt_ctg: type[DeleteCategoryListKeyboardBuilder]
    crt_quiz: type[CreateQuizCategoryListKeyboardBuilder]
    dlt_quiz: type[DeleteQuizCategoryListKeyboardBuilder]
    crt_quiz_qstn: type[CreateQuizQuestionCategoryListKeyboardBuilder]
    dlt_quiz_qstn: type[DeleteQuizQuestionCategoryListKeyboardBuilder]
    edt_quiz_qstn: type[EditQuizQuestionCategoryListKeyboardBuilder]


CATEGORY_LIST_KEYBOARD_BUILDER_MAP: CategoryListKeyboardBuilerMapType = {
    "menu": CategoryListKeyboardBuilder,
    "crt_rsc": CreateResourceCategoryListKeyboardBuilder,
    "edt_rsc": EditResourceCategoryListKeyboardBuilder,
    "dlt_rsc": DeleteResourceCategoryListKeyboardBuilder,
    "edt_ctg": EditCategoryListKeyboardBuilder,
    "dlt_ctg": DeleteCategoryListKeyboardBuilder,
    "crt_quiz": CreateQuizCategoryListKeyboardBuilder,
    "dlt_quiz": DeleteQuizCategoryListKeyboardBuilder,
    "crt_quiz_qstn": CreateQuizQuestionCategoryListKeyboardBuilder,
    "dlt_quiz_qstn": DeleteQuizQuestionCategoryListKeyboardBuilder,
    "edt_quiz_qstn": EditQuizQuestionCategoryListKeyboardBuilder,
}


class ResoruceListKeyboardBuilderMapType(TypedDict):
    menu: type[CategoryResourceListKeyboardBuilder]
    edt_rsc: type[EditResourceResourceListKeyboardBuilder]
    dlt_rsc: type[DeleteResourceResourceListKeyboardBuilder]
    crt_quiz: type[CreateQuizResourceListKeyboardBuilder]
    dlt_quiz: type[DeleteQuizResourceListKeyboardBuilder]
    edt_quiz_qst: type[EditQuizQuestionResourceListKeyboardBuilder]
    crt_quiz_qst: type[CreateQuizQuestionResourceListKeyboardBuilder]
    dlt_quiz_qst: type[DeleteQuizQuestionResourceListKeyboardBuilder]


RESOURCE_LIST_KEYBOARD_BUILDER_MAP: ResoruceListKeyboardBuilderMapType = {
    "menu": CategoryResourceListKeyboardBuilder,
    "edt_rsc": EditResourceResourceListKeyboardBuilder,
    "dlt_rsc": DeleteResourceResourceListKeyboardBuilder,
    "crt_quiz": CreateQuizResourceListKeyboardBuilder,
    "dlt_quiz": DeleteQuizResourceListKeyboardBuilder,
    "edt_quiz_qst": EditQuizQuestionResourceListKeyboardBuilder,
    "crt_quiz_qst": CreateQuizQuestionResourceListKeyboardBuilder,
    "dlt_quiz_qst": DeleteQuizQuestionResourceListKeyboardBuilder,
}


class ResourceItemKeyboardBuilderMapType(TypedDict):
    menu: type[ResourceItemKeyboardBuilder]
    srch: type[SearchResourceItemKeyboardBuilder]


RESOURCE_ITEM_KEYBOARD_BUILDER_MAP: ResourceItemKeyboardBuilderMapType = {
    "menu": ResourceItemKeyboardBuilder,
    "srch": SearchResourceItemKeyboardBuilder,
}

CREATE_RESOURCE_CATEGORIES_ON_PAGE = 5
EDIT_RESOURCE_CATEGORIES_ON_PAGE = 5
EDIT_RESOURCE_RESOURCES_ON_PAGE = 5
DELETE_RESOURCE_CATEGORIES_ON_PAGE = 5
DELETE_RESOURCE_RESOURCES_ON_PAGE = 5
DELETE_CATEGORY_CATEGORIES_ON_PAGE = 5
EDIT_CATEGORY_CATEGORIES_ON_PAGE = 5
LIST_RESOURCES_CATEGORIES_ON_PAGE = 5
EDIT_QUIZ_CATEGORIES_ON_PAGE = 5

CREATE_QUIZ_CATEGORIES_ON_PAGE = 5
CREATE_QUIZ_RESOURCES_ON_PAGE = 5
DELETE_QUIZ_CATEGORIES_ON_PAGE = 5
DELETE_QUIZ_RESOURCES_ON_PAGE = 5
EDIT_QUIZ_RESOURCES_ON_PAGE = 5

LIST_RESOURCES_RESOURCES_ON_PAGE = 5

SEARCH_RESOURCES_RESOURCES_ON_PAGE = 5
