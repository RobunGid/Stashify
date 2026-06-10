from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import selectinload

from database.models.favorite import FavoriteModel
from database.models.quiz import QuizModel
from database.models.resource_item import ResourceItemModel
from database.orm import AsyncSessionLocal
from schemas.resource_schema import ResourceSchema


class ResourceManager:
    FIND_COLUMNS = [
        ResourceItemModel.links,
        ResourceItemModel.description,
        ResourceItemModel.tags,
        ResourceItemModel.name,
    ]

    @classmethod
    async def create(cls, resource_data: ResourceSchema):
        async with AsyncSessionLocal() as session:
            resource = ResourceItemModel(
                **resource_data.model_dump(exclude={"category", "quiz"}),
            )
            session.add(resource)
            await session.commit()

    @classmethod
    async def delete(cls, resource_item_id: UUID):
        async with AsyncSessionLocal() as session:
            statement = select(ResourceItemModel).where(
                ResourceItemModel.resource_item_id == resource_item_id,
            )
            resource = (await session.execute(statement)).scalars().first()
            if not resource:
                raise ValueError("No such resource")
            await session.delete(resource)
            await session.commit()

    @classmethod
    async def update(cls, resource_data: ResourceSchema):
        async with AsyncSessionLocal() as session:
            statement = (
                update(ResourceItemModel)
                .where(ResourceItemModel.resource_item_id == resource_data.resource_item_id)
                .values(**resource_data.model_dump())
            )
            await session.execute(statement)
            await session.commit()

    @classmethod
    async def get_one(cls, resource_item_id: UUID) -> ResourceSchema | None:
        async with AsyncSessionLocal() as session:
            statement = select(ResourceItemModel).where(
                ResourceItemModel.resource_item_id == resource_item_id,
            )

            resource = (await session.execute(statement)).scalars().first()

            if resource is None:
                return None

            return ResourceSchema.model_validate(resource, from_attributes=True)

    @classmethod
    async def get_many(
        cls,
        category_id: Optional[UUID] = None,
        has_quiz: Optional[bool] = None,
        text: Optional[str] = None,
        favorites_user_id: Optional[str] = None,
    ) -> List[ResourceSchema]:
        async with AsyncSessionLocal() as session:
            statement = (
                select(ResourceItemModel)
                .options(
                    selectinload(ResourceItemModel.category),
                )
                .options(
                    selectinload(ResourceItemModel.quiz).selectinload(QuizModel.questions),
                )
                .options(
                    selectinload(ResourceItemModel.ratings),
                )
            )

            if has_quiz is not None:
                if has_quiz:
                    statement = statement.filter(ResourceItemModel.quiz.is_(None))
                else:
                    statement = statement.filter(ResourceItemModel.quiz.is_(None))

            if category_id:
                statement = statement.where(ResourceItemModel.category_id == category_id)

            if text:
                statement = statement.filter(
                    or_(
                        *[func.lower(col).contains(text.lower()) for col in cls.FIND_COLUMNS],
                    ),
                )

            if favorites_user_id:
                statement = statement.join(
                    FavoriteModel,
                    FavoriteModel.resource_item_id == ResourceItemModel.resource_item_id,
                ).where(FavoriteModel.user_id == favorites_user_id)

            resources = (await session.execute(statement)).unique().scalars().all()

            return [ResourceSchema.model_validate(resource, from_attributes=True) for resource in resources]
