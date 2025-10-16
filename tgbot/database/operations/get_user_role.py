from typing import cast
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.user import Role, UserModel

async def get_user_role(user_id: str) -> Role:
    async with AsyncSessionLocal() as session:
        statement = select(UserModel).where(UserModel.id==user_id)
        user = (await session.execute(statement)).scalars().first()
        
        return cast(Role, user.role) if user else Role.user