from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.models.user import Role
from database.operations.get_user_role import get_user_role

class UserRoleFilter(BaseFilter):
    def __init__(self, roles: List[Role]):
        self.roles = roles
        
    async def __call__(self, message: Message) -> bool:
        user_role = await get_user_role(str(message.from_user.id)) if message.from_user else None
        return user_role in self.roles
