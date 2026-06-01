from typing import TypeVar, Protocol, Type, Generic

from pydantic import UUID4, BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import Mapped

from database.orm import AsyncSessionLocal

class HasId(Protocol):
    id: Mapped[int]

T = TypeVar("T", bound=HasId)
S = TypeVar("S", bound=BaseModel)

class BaseManager(Generic[T, S]):
    model: Type[T] | None = None
    schema: Type[BaseModel] | None = None
    
    @classmethod
    async def get_one(cls, item_id: UUID4):
        if cls.model is None:
            raise AttributeError("No model provided")
        if cls.schema is None:
            raise AttributeError("No schema provided")
        async with AsyncSessionLocal() as session:
            statement = select(cls.model)\
                .where(
                    cls.model.id == item_id
                )
            
            item = (await session.execute(statement)).scalars().first()
            
            if item is None:
                return None
            
            return cls.schema.model_validate(item, from_attributes=True)
     
    @classmethod    
    async def create(cls, data: BaseModel):
        async with AsyncSessionLocal() as session:
            if cls.model is None:
                raise AttributeError("No model provided")
            item = cls.model(**data.model_dump())
            session.add(item)
            await session.commit()
            
    @classmethod
    async def update(cls, id: UUID4, new_data: BaseModel) -> None:
        async with AsyncSessionLocal() as session:
            if cls.model is None:
                raise AttributeError("No model provided")
            statement = update(cls.model).where(cls.model.id==id).values(
                **new_data.model_dump()
            )
            await session.execute(statement)
            await session.commit()
            
    @classmethod
    async def delete(cls, id: UUID4) -> None:
        async with AsyncSessionLocal() as session:
            if cls.model is None:
                raise AttributeError("No model provided")
            statement = select(cls.model).where(cls.model.id==id)
            category = (await session.execute(statement)).scalars().first()
            if not category:
                raise ValueError("No such category")
            await session.delete(category)
            await session.commit()