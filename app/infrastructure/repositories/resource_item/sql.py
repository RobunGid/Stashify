from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.resource_item import ResourceItemModel
from infrastructure.repositories.base import GetManyResult, SQLAlchemyRepositoryMixin
from infrastructure.repositories.resource_item.base import BaseResourceItemRepository
from sqlalchemy import func, select, Update


@dataclass
class SQLResourceItemRepository(BaseResourceItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_item: ResourceItemEntity) -> None:
        item = ResourceItemModel(resource_item)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_item_id: UUID) -> ResourceItemEntity | None:
        statement = select(CategoryItemModel).where(
            ResourceItemModel.resource_item_id == resource_item_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return ResourceItemEntity(**item)

    async def get_many(self, filters: ResourceItemFilters) -> GetManyResult[ResourceItemEntity]:

        statement = select(ResourceItemModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        resource_items = (await self.session.execute(statement)).scalars().all()
        resource_items_entities = [ResourceItemEntity(**category) for category in resource_items]
        return GetManyResult(items=resource_items_entities, total=total)

    async def delete(self, resource_item_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.resource_item_id == resource_item_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_item_id: UUID, resource_item: ResourceItemUpdateEntity) -> None:
        statement = (
            Update(CategoryItemModel)
            .where(CategoryItemModel.resource_item_id == resource_item_id)
            .values(**{k: v for k, v in asdict(resource_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
