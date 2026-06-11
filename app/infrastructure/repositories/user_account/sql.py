from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from domain.filters.user_account import UserAccountFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.user_account import UserAccountModel
from infrastructure.repositories.base import GetManyResult, SQLAlchemyRepositoryMixin
from infrastructure.repositories.user_account.base import BaseUserAccountRepository
from sqlalchemy import func, select, Update


@dataclass
class SQLUserAccountRepository(BaseUserAccountRepository, SQLAlchemyRepositoryMixin):
    async def create(self, user_account: UserAccountEntity) -> None:
        item = UserAccountModel(user_account)
        self.session.add(item)
        await self.session.commit()

    async def get_one(self, user_account_id: UUID) -> UserAccountEntity | None:
        statement = select(CategoryItemModel).where(
            UserAccountModel.user_account_id == user_account_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return UserAccountEntity(**item)

    async def get_many(self, filters: UserAccountFilters) -> GetManyResult[UserAccountEntity]:

        statement = select(UserAccountModel)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = (await self.session.execute(count_statement)).scalar_one()

        if filters.offset is not None:
            statement = statement.offset(filters.offset)
        if filters.count is not None:
            statement = statement.limit(filters.count)

        user_accounts = (await self.session.execute(statement)).scalars().all()
        user_accounts_entities = [UserAccountEntity(**category) for category in user_accounts]
        return GetManyResult(items=user_accounts_entities, total=total)

    async def delete(self, user_account_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.user_account_id == user_account_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, user_account_id: UUID, user_account: UserAccountUpdateEntity) -> None:
        statement = (
            Update(CategoryItemModel)
            .where(CategoryItemModel.user_account_id == user_account_id)
            .values(**{k: v for k, v in asdict(user_account).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()
