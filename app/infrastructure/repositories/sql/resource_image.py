from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.resource_image import ResourceImageEntity, ResourceImageUpdateEntity
from domain.filters.resource_image import ResourceImageFilters
from domain.repositories.resource_image import BaseResourceImageRepository
from infrastructure.mappers.resource_image import ResourceImageMapper
from infrastructure.models.resource_image import ResourceImageModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import func, select, update


@dataclass
class SQLResourceImageRepository(BaseResourceImageRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_image: ResourceImageEntity) -> None:
        item = ResourceImageMapper.to_model(resource_image)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_image_id: UUID) -> ResourceImageEntity | None:
        statement = select(ResourceImageModel).where(
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

        resource_image_models = (await self.session.execute(statement)).scalars().all()
        resource_images_entities = [
            ResourceImageMapper.to_entity(resource_image_model) for resource_image_model in resource_image_models
        ]
        return GetManyResult(items=resource_images_entities, total=total)

    async def delete_by_id(self, resource_image_id: UUID) -> None:
        statement = select(ResourceImageModel).where(ResourceImageModel.resource_image_id == resource_image_id)
        resource_image_model = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(resource_image_model)
        await self.session.commit()

    async def update(self, resource_image_id: UUID, resource_image: ResourceImageUpdateEntity) -> None:
        statement = (
            update(ResourceImageModel)
            .where(ResourceImageModel.resource_image_id == resource_image_id)
            .values(**{k: v for k, v in asdict(resource_image).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
