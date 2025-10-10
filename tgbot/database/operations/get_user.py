from typing import cast
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.user import Role, UserModel
from schemas.user_schema import UserSchema

async def get_user(tg_user_id: str) -> UserSchema:
    async with AsyncSessionLocal() as session:
        statement = select(UserModel).where(UserModel.tg_id==tg_user_id).options(
            selectinload(UserModel.quiz_results)
        )\
        .options(
            selectinload(UserModel.quiz_ratings)
        )
        
        user = (await session.execute(statement)).scalars().first()
        
        return UserSchema.model_validate(user, from_attributes=True)