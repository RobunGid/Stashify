from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.orm import AsyncSessionLocal
from database.models.user import UserModel
from schemas.user_schema import UserSchema

class UserManager:
    @classmethod
    async def get_user(cls, user_id: str) -> UserSchema:
        async with AsyncSessionLocal() as session:
            statement = select(UserModel).where(UserModel.id==user_id).options(
                selectinload(UserModel.quiz_results)
            )\
            .options(
                selectinload(UserModel.quiz_ratings)
            )
            
            user = (await session.execute(statement)).scalars().first()
            
            return UserSchema.model_validate(user, from_attributes=True)
    
    @classmethod
    async def create_user(cls, user_data: UserSchema):
        async with AsyncSessionLocal() as session:
            statement = select(UserModel).where(UserModel.id==user_data.id)
            existing_user = (await session.execute(statement)).scalars().first()
            if existing_user: 
                return
            
            user = UserModel(**user_data.model_dump())
            session.add(user)
            await session.commit()