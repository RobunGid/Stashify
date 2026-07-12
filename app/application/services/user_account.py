from application.services.base import BaseService
from domain.entities.user_account import UserAccountEntity, UserAccountUpdateEntity
from domain.filters.user_account import UserAccountFilters
from domain.repositories.user_account import BaseUserAccountRepository


class UserAccountService(BaseService[UserAccountEntity, UserAccountUpdateEntity, UserAccountFilters]):
    repository: BaseUserAccountRepository

    async def get_one_by_telegram_id(self, telegram_id: int) -> UserAccountEntity | None:
        return await self.repository.get_one_by_telegram_id(telegram_id)
