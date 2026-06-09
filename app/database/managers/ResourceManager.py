from typing import List, Optional

from pydantic import UUID4
from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import selectinload

from database.models.favorite import FavoriteModel
from database.models.quiz import QuizModel
from database.models.resource import ResourceModel
from database.orm import AsyncSessionLocal
from schemas.resource_schema import ResourceSchema


class ResourceManager:
    FIND_COLUMNS = [
        ResourceModel.links,
        ResourceModel.description,
        ResourceModel.tags,
        ResourceModel.name,
    ]

    @classmethod
    async def create(cls, resource_data: ResourceSchema):
        async with AsyncSessionLocal() as session:
            resource = ResourceModel(
                **resource_data.model_dump(exclude={"category", "quiz"}),
            )
            session.add(resource)
            await session.commit()

    @classmethod
    async def delete(cls, id: UUID4):
        async with AsyncSessionLocal() as session:
            statement = select(ResourceModel).where(ResourceModel.resource_id == id)
            resource = (await session.execute(statement)).scalars().first()
            if not resource:
                raise ValueError("No such resource")
            await session.delete(resource)
            await session.commit()

    @classmethod
    async def update(cls, resource_data: ResourceSchema):
        async with AsyncSessionLocal() as session:
            statement = (
                update(ResourceModel)
                .where(ResourceModel.resource_id == resource_data.resource_id)
                .values(**resource_data.model_dump())
            )
            await session.execute(statement)
            await session.commit()

    @classmethod
    async def get_one(cls, resource_id: UUID4) -> ResourceSchema | None:
        async with AsyncSessionLocal() as session:
            statement = select(ResourceModel).where(
                ResourceModel.resource_id == resource_id,
            )

            resource = (await session.execute(statement)).scalars().first()

            if resource is None:
                return None

            return ResourceSchema.model_validate(resource, from_attributes=True)

    @classmethod
    async def get_many(
        cls,
        category_id: Optional[UUID4] = None,
        has_quiz: Optional[bool] = None,
        text: Optional[str] = None,
        favorites_user_id: Optional[str] = None,
    ) -> List[ResourceSchema]:
        async with AsyncSessionLocal() as session:
            statement = (
                select(ResourceModel)
                .options(
                    selectinload(ResourceModel.category),
                )
                .options(
                    selectinload(ResourceModel.quiz).selectinload(QuizModel.questions),
                )
                .options(
                    selectinload(ResourceModel.ratings),
                )
            )

            if has_quiz is not None:
                if has_quiz:
                    statement = statement.filter(ResourceModel.quiz.is_(None))
                else:
                    statement = statement.filter(ResourceModel.quiz.is_(None))

            if category_id:
                statement = statement.where(ResourceModel.category_id == category_id)

            if text:
                statement = statement.filter(
                    or_(
                        *[func.lower(col).contains(text.lower()) for col in cls.FIND_COLUMNS],
                    ),
                )

            if favorites_user_id:
                statement = statement.join(
                    FavoriteModel,
                    FavoriteModel.resource_id == ResourceModel.resource_id,
                ).where(FavoriteModel.user_id == favorites_user_id)

            resources = (await session.execute(statement)).unique().scalars().all()

            return [ResourceSchema.model_validate(resource, from_attributes=True) for resource in resources]
