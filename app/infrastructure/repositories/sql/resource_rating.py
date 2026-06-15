from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters
from domain.repositories.resource_rating import BaseResourceRatingRepository
from infrastructure.mappers.resource_rating import ResourceRatingMapper
from infrastructure.models.resource_rating import ResourceRatingModel
from infrastructure.repositories.sql.base import SQLAlchemyRepositoryMixin
from sqlalchemy import and_, func, select, update


@dataclass
class SQLResourceRatingRepository(BaseResourceRatingRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_rating: ResourceRatingEntity) -> None:
        item = ResourceRatingModel(resource_rating)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_rating_id: UUID) -> ResourceRatingEntity | None:
        statement = select(ResourceRatingModel).where(
            ResourceRatingModel.resource_rating_id == resource_rating_id,
        )

        resource_rating_model = (await self.session.execute(statement)).scalars().first()

        if resource_rating_model is None:
            return None

        return ResourceRatingMapper.to_entity(resource_rating_model)

    async def get_many(self, filters: ResourceRatingFilters) -> GetManyResult[ResourceRatingEntity]:

        statement = select(ResourceRatingModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        resource_rating_models = (await self.session.execute(statement)).scalars().all()
        resource_ratings_entities = [
            ResourceRatingMapper.to_entity(resource_rating_model) for resource_rating_model in resource_rating_models
        ]
        return GetManyResult(items=resource_ratings_entities, total=total)

    async def delete_by_id(self, resource_rating_id: UUID) -> None:
        statement = select(ResourceRatingModel).where(ResourceRatingModel.resource_rating_id == resource_rating_id)
        resource_rating_model = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(resource_rating_model)
        await self.session.commit()

    async def update(self, resource_rating_id: UUID, resource_rating: ResourceRatingUpdateEntity) -> None:
        statement = (
            update(ResourceRatingModel)
            .where(ResourceRatingModel.resource_rating_id == resource_rating_id)
            .values(**{k: v for k, v in asdict(resource_rating).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def delete_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> None:
        statement = select(ResourceRatingModel).where(
            and_(
                ResourceRatingModel.user_account_id == user_account_id,
                ResourceRatingModel.resource_item_id == resource_item_id,
            ),
        )
        resource_rating_model = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(resource_rating_model)
        await self.session.commit()

    async def get_one_by_user_account_id_and_resource_item_id(
        self,
        user_account_id: UUID,
        resource_item_id: UUID,
    ) -> ResourceRatingEntity | None:
        statement = select(ResourceRatingModel).where(
            and_(
                ResourceRatingModel.user_account_id == user_account_id,
                ResourceRatingModel.resource_item_id == resource_item_id,
            ),
        )

        resource_rating_model = (await self.session.execute(statement)).scalars().first()

        if resource_rating_model is None:
            return None

        return ResourceRatingMapper.to_entity(resource_rating_model)

    async def get_count(self, filters: ResourceRatingFilters) -> int:

        statement = select(ResourceRatingModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        return total
