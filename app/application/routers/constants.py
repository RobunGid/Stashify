from typing import TypedDict

from application.keyboards.categories import DeleteCategoryListKeyboardBuilder, EditCategoryListKeyboardBuilder
from application.keyboards.menu import (
    AdminMenuKeyboardBuilder,
    BaseMenuKeyboardBuilder,
    ManagerMenuKeyboardBuilder,
    UserMenuKeyboardBuilder,
)
from application.keyboards.quizes import (
    CreateQuizCategoryListKeyboardBuilder,
    CreateQuizResourceListKeyboardBuilder,
    DeleteQuizCategoryListKeyboardBuilder,
    DeleteQuizResourceListKeyboardBuilder,
    EditQuizCategoryListKeyboardBuilder,
    EditQuizResourceListKeyboardBuilder,
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
    crt_qz: type[CreateQuizCategoryListKeyboardBuilder]
    edt_qz: type[EditQuizCategoryListKeyboardBuilder]
    dlt_qz: type[DeleteQuizCategoryListKeyboardBuilder]


CATEGORY_LIST_KEYBOARD_BUILDER_MAP: CategoryListKeyboardBuilerMapType = {
    "menu": CategoryListKeyboardBuilder,
    "crt_rsc": CreateResourceCategoryListKeyboardBuilder,
    "edt_rsc": EditResourceCategoryListKeyboardBuilder,
    "dlt_rsc": DeleteResourceCategoryListKeyboardBuilder,
    "edt_ctg": EditCategoryListKeyboardBuilder,
    "dlt_ctg": DeleteCategoryListKeyboardBuilder,
    "crt_qz": CreateQuizCategoryListKeyboardBuilder,
    "edt_qz": EditQuizCategoryListKeyboardBuilder,
    "dlt_qz": DeleteQuizCategoryListKeyboardBuilder,
}


class ResoruceListKeyboardBuilderMapType(TypedDict):
    menu: type[CategoryResourceListKeyboardBuilder]
    edt_rsc: type[EditResourceResourceListKeyboardBuilder]
    dlt_rsc: type[DeleteResourceResourceListKeyboardBuilder]
    crt_qz: type[CreateQuizResourceListKeyboardBuilder]
    edt_qz: type[EditQuizResourceListKeyboardBuilder]
    dlt_qz: type[DeleteQuizResourceListKeyboardBuilder]


RESOURCE_LIST_KEYBOARD_BUILDER_MAP: ResoruceListKeyboardBuilderMapType = {
    "menu": CategoryResourceListKeyboardBuilder,
    "edt_rsc": EditResourceResourceListKeyboardBuilder,
    "dlt_rsc": DeleteResourceResourceListKeyboardBuilder,
    "crt_qz": CreateQuizResourceListKeyboardBuilder,
    "edt_qz": EditQuizResourceListKeyboardBuilder,
    "dlt_qz": DeleteQuizResourceListKeyboardBuilder,
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
