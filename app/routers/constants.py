from database.models.user import Role
from keyboards.menu import (
    AdminMenuKeyboardBuilder,
    BaseMenuKeyboardBuilder,
    ManagerMenuKeyboardBuilder,
    UserMenuKeyboardBuilder,
)

ROLE_MENU_KEYBOARD_BUILDER_MAP: dict[Role, type[BaseMenuKeyboardBuilder]] = {
    Role.admin: AdminMenuKeyboardBuilder,
    Role.manager: ManagerMenuKeyboardBuilder,
    Role.user: UserMenuKeyboardBuilder,
}
