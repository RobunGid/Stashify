from sqlalchemy import select

from schemas.user_schema import UserSchema
from database.orm import AsyncSessionLocal
from database.models.user import UserModel

async def create_user(user_data: UserSchema):
    async with AsyncSessionLocal() as session:
        statement = select(UserModel).where(UserModel.id==user_data.id)
        existing_user = (await session.execute(statement)).scalars().first()
        if existing_user: return
        
        user = UserModel(**user_data.model_dump())
        session.add(user)
        await session.commit()