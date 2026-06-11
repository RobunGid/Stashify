from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity
from domain.filters.resource_image import ResourceImageFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.resource_image import ResourceImageModel
from infrastructure.repositories.base import GetManyResult, SQLAlchemyRepositoryMixin
from infrastructure.repositories.resource_image.base import BaseResourceImageRepository
from sqlalchemy import func, select, Update


@dataclass
class SQLResourceImageRepository(BaseResourceImageRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_image: ResourceImageEntity) -> None:
        item = ResourceImageModel(resource_image)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_image_id: UUID) -> ResourceImageEntity | None:
        statement = select(CategoryItemModel).where(
            ResourceImageModel.resource_image_id == resource_image_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return ResourceImageEntity(**item)

    async def get_many(self, filters: ResourceImageFilters) -> GetManyResult[ResourceImageEntity]:

        statement = select(ResourceImageModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        resource_images = (await self.session.execute(statement)).scalars().all()
        resource_images_entities = [ResourceImageEntity(**category) for category in resource_images]
        return GetManyResult(items=resource_images_entities, total=total)

    async def delete(self, resource_image_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.resource_image_id == resource_image_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_image_id: UUID, resource_image: ResourceImageUpdateEntity) -> None:
        statement = (
            Update(CategoryItemModel)
            .where(CategoryItemModel.resource_image_id == resource_image_id)
            .values(**{k: v for k, v in asdict(resource_image).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
