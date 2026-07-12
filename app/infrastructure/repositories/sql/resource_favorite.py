from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.resource_favorite import ResourceFavoriteEntity, ResourceFavoriteUpdateEntity
from domain.filters.resource_favorite import ResourceFavoriteFilters
from domain.repositories.resource_favorite import BaseResourceFavoriteRepository
from infrastructure.mappers.resource_favorite import ResourceFavoriteMapper
from infrastructure.models.resource_favorite import ResourceFavoriteModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import and_, exists, func, select, update


@dataclass
class SQLResourceFavoriteRepository(BaseResourceFavoriteRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_favorite: ResourceFavoriteEntity) -> None:
        model = ResourceFavoriteMapper.to_model(resource_favorite)
        self.session.add(model)
        await self.session.commit()

    async def get_one(self, resource_favorite_id: UUID) -> ResourceFavoriteEntity | None:
        statement = select(ResourceFavoriteModel).where(
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

        resource_favorite_models = (await self.session.execute(statement)).scalars().all()
        resource_favorites_entities = [
            ResourceFavoriteMapper.to_entity(model=resource_favorite_model)
            for resource_favorite_model in resource_favorite_models
        ]
        return GetManyResult(items=resource_favorites_entities, total=total)

    async def delete_by_id(self, resource_favorite_id: UUID) -> None:
        statement = select(ResourceFavoriteModel).where(
            ResourceFavoriteModel.resource_favorite_id == resource_favorite_id,
        )
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_favorite_id: UUID, resource_favorite: ResourceFavoriteUpdateEntity) -> None:
        statement = (
            update(ResourceFavoriteModel)
            .where(ResourceFavoriteModel.resource_favorite_id == resource_favorite_id)
            .values(**{k: v for k, v in asdict(resource_favorite).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        statement = select(ResourceFavoriteModel).where(
            and_(
                ResourceFavoriteModel.user_account_id == user_account_id,
                ResourceFavoriteModel.resource_item_id == resource_item_id,
            ),
        )
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def check_exists_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> bool:
        statement = select(
            exists().where(
                ResourceFavoriteModel.user_account_id == user_account_id,
                ResourceFavoriteModel.resource_item_id == resource_item_id,
            ),
        )

        is_exists = (await self.session.execute(statement)).scalars().first()

        return bool(is_exists)

    async def get_count(self, filters: ResourceFavoriteFilters) -> int:

        statement = select(ResourceFavoriteModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
