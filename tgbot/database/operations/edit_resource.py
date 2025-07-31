from pydantic import UUID4
from sqlalchemy import select

from database.orm import AsyncSessionLocal
from database.models.resource import ResourceModel

async def edit_resource(id: UUID4, new_name: str | None = None, new_tags: str | None = None, new_image: str | None = None, new_description: str | None = None) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(ResourceModel).where(ResourceModel.id==id)
        resource = (await session.execute(statement)).scalars().first()
        if not resource:
            raise ValueError("No such resource")
        if new_name:
            resource.name = new_name # type: ignore
        if new_image:
            resource.image = new_image # type: ignore
        if new_description:
            resource.description = new_description # type: ignore
        if new_tags:
            resource.tags = new_tags # type: ignore
        await session.commit()
        