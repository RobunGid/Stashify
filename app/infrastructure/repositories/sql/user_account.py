from dataclasses import asdict, dataclass
from uuid import UUID

from domain.entities.base import GetManyResult
from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from domain.filters.user_account import UserAccountFilters
from infrastructure.models.category_item import CategoryItemModel
from infrastructure.models.user_account import UserAccountModel
from infrastructure.repositories.base import BaseSQLAlchemyRepository
from sqlalchemy import func, select, update


@dataclass
class SQLUserAccountRepository(
    BaseSQLAlchemyRepository[UserAccountEntity, UserAccountUpdateEntity, UserAccountFilters],
):
    async def create(self, user_account: UserAccountEntity) -> None:
        item = UserAccountModel(**user_account.__dict__)
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

    async def delete_by_id(self, user_account_id: UUID) -> None:
        statement = select(CategoryItemModel).where(CategoryItemModel.user_account_id == user_account_id)
        category = (await self.session.execute(statement)).scalars().first()
        await self.session.delete(category)
        await self.session.commit()

    async def update(self, user_account_id: UUID, user_account: UserAccountUpdateEntity) -> None:
        statement = (
            update(CategoryItemModel)
            .where(CategoryItemModel.user_account_id == user_account_id)
            .values(**{k: v for k, v in asdict(user_account).items() if v is not None})
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_one_by_telegram_id(self, user_telegram_id: int) -> UserAccountEntity | None:
        statement = select(UserAccountModel).where(
            UserAccountModel.user_telegram_id == user_telegram_id,
        )

        item = (await self.session.execute(statement)).scalars().first()

        if item is None:
            return None

        return UserAccountEntity(
            created_at=item.created_at,
            user_account_id=item.user_account_id,
            username=item.username,
            user_telegram_id=item.user_telegram_id,
            role=item.role,
        )
