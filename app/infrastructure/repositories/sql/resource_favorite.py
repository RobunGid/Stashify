from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.resource_favorite import ResourceFavoriteModel
from infrastructure.repositories.base import BaseSQLAlchemyRepository
from sqlalchemy import func, select, update


@dataclass
class SQLResourceFavoriteRepository(
    BaseSQLAlchemyRepository[ResourceFavoriteEntity, ResourceFavoriteUpdateEntity, ResourceFavoriteFilters]
):
    async def create(self, resource_favorite: ResourceFavoriteEntity) -> None:
        item = ResourceFavoriteModel(resource_favorite)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_favorite_id: UUID) -> ResourceFavoriteEntity | None:
        statement = select(CategoryItemModel).where(
            ResourceFavoriteModel.resource_favorite_id == resource_favorite_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return ResourceFavoriteEntity(**item)

    async def get_many(self, filters: ResourceFavoriteFilters) -> GetManyResult[ResourceFavoriteEntity]:

        statement = select(ResourceFavoriteModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        resource_favorites = (await self.session.execute(statement)).scalars().all()
        resource_favorites_entities = [ResourceFavoriteEntity(**category) for category in resource_favorites]
        return GetManyResult(items=resource_favorites_entities, total=total)

    async def delete(self, resource_favorite_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.resource_favorite_id == resource_favorite_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_favorite_id: UUID, resource_favorite: ResourceFavoriteUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.resource_favorite_id == resource_favorite_id)
            .values(**{k: v for k, v in asdict(resource_favorite).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
