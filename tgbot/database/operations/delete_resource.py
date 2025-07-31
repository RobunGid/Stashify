from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel

async def delete_resource(id: UUID4) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel).where(ResourceModel.id==id)
        resource = (await session.execute(statement)).scalars().first()
        if not resource:
            raise ValueError("No such resource")
        await session.delete(resource)
        await session.commit()
        