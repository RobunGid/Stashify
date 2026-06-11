from dishka import AnyOf, provide, Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.quiz_item.base import BaseQuizItemRepository
from infrastructure.repositories.quiz_item.sql import SQLQuizItemRepository

from infrastructure.repositories.quiz_rating.base import BaseQuizRatingRepository
from infrastructure.repositories.quiz_rating.sql import SQLQuizRatingRepository

from infrastructure.repositories.resource_favorite.base import BaseResourceFavoriteRepository
from infrastructure.repositories.resource_favorite.sql import SQLResourceFavoriteRepository

from infrastructure.repositories.resource_item.base import BaseResourceItemRepository
from infrastructure.repositories.resource_item.sql import SQLResourceItemRepository

from infrastructure.repositories.user_account.base import BaseUserAccountRepository
from infrastructure.repositories.user_account.sql import SQLUserAccountRepository

from infrastructure.repositories.category_item.base import BaseCategoryItemRepository
from infrastructure.repositories.category_item.sql import SQLCategoryItemRepository

from infrastructure.repositories.quiz_question.base import BaseQuizQuestionRepository
from infrastructure.repositories.quiz_question.sql import SQLQuizQuestionRepository

from infrastructure.repositories.quiz_result.base import BaseQuizResultRepository
from infrastructure.repositories.quiz_result.sql import SQLQuizResultRepository

from infrastructure.repositories.resource_image.base import BaseResourceImageRepository
from infrastructure.repositories.resource_image.sql import SQLResourceImageRepository

from infrastructure.repositories.resource_rating.base import BaseResourceRatingRepository
from infrastructure.repositories.resource_rating.sql import SQLResourceRatingRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_category_items_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseCategoryItemRepository, SQLCategoryItemRepository]:
        return SQLCategoryItemRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_quiz_item_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseQuizItemRepository, SQLQuizItemRepository]:
        return SQLQuizItemRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_quiz_rating_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseQuizRatingRepository, SQLQuizRatingRepository]:
        return SQLQuizRatingRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_resource_favorite_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseResourceFavoriteRepository, SQLResourceFavoriteRepository]:
        return SQLResourceFavoriteRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_resource_item_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseResourceItemRepository, SQLResourceItemRepository]:
        return SQLResourceItemRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_user_account_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseUserAccountRepository, SQLUserAccountRepository]:
        return SQLUserAccountRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_quiz_question_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseQuizQuestionRepository, SQLQuizQuestionRepository]:
        return SQLQuizQuestionRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_quiz_result_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseQuizResultRepository, SQLQuizResultRepository]:
        return SQLQuizResultRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_resource_image_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseResourceImageRepository, SQLResourceImageRepository]:
        return SQLResourceImageRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_resource_rating_repository(
        self,
        session: AsyncSession,
    ) -> AnyOf[BaseResourceRatingRepository, SQLResourceRatingRepository]:
        return SQLResourceRatingRepository(session=session)
