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
)
from infrastructure.models.user_account import Role

ROLE_MENU_KEYBOARD_BUILDER_MAP: dict[Role, type[BaseMenuKeyboardBuilder]] = {
    Role.admin: AdminMenuKeyboardBuilder,
    Role.manager: ManagerMenuKeyboardBuilder,
    Role.user: UserMenuKeyboardBuilder,
}

CATEGORY_LIST_KEYBOARD_BUILDER_MAP = {
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

RESOURCE_LIST_KEYBOARD_BUILDER_MAP = {
    "menu": CategoryResourceListKeyboardBuilder,
    "edt_rsc": EditResourceResourceListKeyboardBuilder,
    "dlt_rsc": DeleteResourceResourceListKeyboardBuilder,
    "crt_qz": CreateQuizResourceListKeyboardBuilder,
    "edt_qz": EditQuizResourceListKeyboardBuilder,
    "dlt_qz": DeleteQuizResourceListKeyboardBuilder,
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
