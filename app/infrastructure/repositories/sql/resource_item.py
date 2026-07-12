from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from domain.filters.resource_item import ResourceItemFilters
from domain.repositories.resource_item import BaseResourceItemRepository
from infrastructure.mappers.resource_item import ResourceItemMapper
from infrastructure.models.resource_item import ResourceItemModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import func, or_, select, update


@dataclass
class SQLResourceItemRepository(BaseResourceItemRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_item: ResourceItemEntity) -> None:
        item = ResourceItemMapper.to_model(resource_item)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_item_id: UUID) -> ResourceItemEntity | None:
        statement = select(ResourceItemModel).where(
            ResourceItemModel.resource_item_id == resource_item_id,
        )

        resource_item_model = (await self.session.execute(statement)).scalars().first()

        if resource_item_model is None:
            return None

        return ResourceItemMapper.to_entity(resource_item_model)

    async def get_many(self, filters: ResourceItemFilters) -> GetManyResult[ResourceItemEntity]:

        statement = select(ResourceItemModel)

        if filters.category_item_id is not None:
            statement = statement.where(ResourceItemModel.category_item_id == filters.category_item_id)

        if filters.query is not None:
            statement = statement.where(
                or_(
                    ResourceItemModel.name.ilike(f"%{filters.query}%"),
                    ResourceItemModel.description.ilike(f"%{filters.query}%"),
                    ResourceItemModel.links.ilike(f"%{filters.query}%"),
                    ResourceItemModel.tags.ilike(f"%{filters.query}%"),
                ),
            )

        count_statement = select(func.count()).select_from(statement.subquery())

        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        match filters.sort:
            case "created_at":
                statement = statement.order_by(getattr(ResourceItemModel.created_at, filters.order.value)())
            case "updated_at":
                statement = statement.order_by(getattr(ResourceItemModel.updated_at, filters.order.value)())
            case "name":
                statement = statement.order_by(getattr(ResourceItemModel.name, filters.order.value)())

        resource_items = (await self.session.execute(statement)).unique().scalars().all()
        resource_items_entities = [
            ResourceItemMapper.to_entity(resource_item_model) for resource_item_model in resource_items
        ]
        return GetManyResult(items=resource_items_entities, total=total)

    async def delete_by_id(self, resource_item_id: UUID) -> None:
        statement = select(ResourceItemModel).where(ResourceItemModel.resource_item_id == resource_item_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_item_id: UUID, resource_item: ResourceItemUpdateEntity) -> None:
        statement = (
            update(ResourceItemModel)
            .where(ResourceItemModel.resource_item_id == resource_item_id)
            .values(**{k: v for k, v in asdict(resource_item).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_resource_item_index_by_filters(
        self,
        resource_item_id: UUID,
        filters: ResourceItemFilters,
    ) -> int | None:

        match filters.sort:
            case "created_at":
                order_by_field = getattr(ResourceItemModel.created_at, filters.order.value)()
            case "updated_at":
                order_by_field = getattr(ResourceItemModel.updated_at, filters.order.value)()
            case "name":
                order_by_field = getattr(ResourceItemModel.name, filters.order.value)()

        subquery = select(
            ResourceItemModel.resource_item_id,
            (func.row_number().over(order_by=order_by_field) - 1).label("position"),
        )

        if filters.category_item_id is not None:
            subquery = subquery.where(ResourceItemModel.category_item_id == filters.category_item_id)

        if filters.query is not None:
            subquery = subquery.where(
                or_(
                    ResourceItemModel.name.ilike(f"%{filters.query}%"),
                    ResourceItemModel.description.ilike(f"%{filters.query}%"),
                    ResourceItemModel.links.ilike(f"%{filters.query}%"),
                    ResourceItemModel.tags.ilike(f"%{filters.query}%"),
                ),
            )

        subquery = subquery.subquery()

        statement = select(subquery.c.position).where(subquery.c.resource_item_id == resource_item_id)

        result = await self.session.execute(statement)
        index = result.scalar_one_or_none()

        return int(index) if index is not None else None

    async def get_count(self, filters: ResourceItemFilters) -> int:

        statement = select(ResourceItemModel)

        if filters.category_item_id is not None:
            statement = statement.where(ResourceItemModel.category_item_id == filters.category_item_id)

        if filters.query is not None:
            statement = statement.where(
                or_(
                    ResourceItemModel.name.ilike(f"%{filters.query}%"),
                    ResourceItemModel.description.ilike(f"%{filters.query}%"),
                    ResourceItemModel.links.ilike(f"%{filters.query}%"),
                    ResourceItemModel.tags.ilike(f"%{filters.query}%"),
                ),
            )

        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
