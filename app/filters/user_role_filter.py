from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.models.user import Role
from database.managers.UserManager import UserManager

class UserRoleFilter(BaseFilter):
    def __init__(self, roles: List[Role]):
        self.roles = roles
        
    async def __call__(self, message: Message) -> bool:
        if not message.from_user or not message.from_user.id: 
            return False
        user = await UserManager.get_one(str(message.from_user.id))
        user_role = user.role
        return user_role in self.roles
