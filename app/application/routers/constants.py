from application.keyboards.menu import (
    AdminMenuKeyboardBuilder,
    BaseMenuKeyboardBuilder,
    ManagerMenuKeyboardBuilder,
    UserMenuKeyboardBuilder,
)
from infrastructure.models.user_account import Role

ROLE_MENU_KEYBOARD_BUILDER_MAP: dict[Role, type[BaseMenuKeyboardBuilder]] = {
    Role.admin: AdminMenuKeyboardBuilder,
    Role.manager: ManagerMenuKeyboardBuilder,
    Role.user: UserMenuKeyboardBuilder,
}
