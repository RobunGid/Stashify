from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.resource_rating import ResourceRatingEntity, ResourceRatingUpdateEntity
from domain.filters.resource_rating import ResourceRatingFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.resource_rating import ResourceRatingModel
from infrastructure.repositories.base import GetManyResult, SQLAlchemyRepositoryMixin
from infrastructure.repositories.resource_rating.base import BaseResourceRatingRepository
from sqlalchemy import func, select, Update


@dataclass
class SQLResourceRatingRepository(BaseResourceRatingRepository, SQLAlchemyRepositoryMixin):
    async def create(self, resource_rating: ResourceRatingEntity) -> None:
        item = ResourceRatingModel(resource_rating)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, resource_rating_id: UUID) -> ResourceRatingEntity | None:
        statement = select(CategoryItemModel).where(
            ResourceRatingModel.resource_rating_id == resource_rating_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return ResourceRatingEntity(**item)

    async def get_many(self, filters: ResourceRatingFilters) -> GetManyResult[ResourceRatingEntity]:

        statement = select(ResourceRatingModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        resource_ratings = (await self.session.execute(statement)).scalars().all()
        resource_ratings_entities = [ResourceRatingEntity(**category) for category in resource_ratings]
        return GetManyResult(items=resource_ratings_entities, total=total)

    async def delete(self, resource_rating_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.resource_rating_id == resource_rating_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, resource_rating_id: UUID, resource_rating: ResourceRatingUpdateEntity) -> None:
        statement = (
            Update(CategoryItemModel)
            .where(CategoryItemModel.resource_rating_id == resource_rating_id)
            .values(**{k: v for k, v in asdict(resource_rating).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
