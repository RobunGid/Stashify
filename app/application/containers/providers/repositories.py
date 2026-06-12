from dishka import AnyOf, provide, Provider, Scope
from domain.repositories.category_item import BaseCategoryItemRepository
from domain.repositories.quiz_item import BaseQuizItemRepository
from domain.repositories.quiz_question import BaseQuizQuestionRepository
from domain.repositories.quiz_rating import BaseQuizRatingRepository
from domain.repositories.quiz_result import BaseQuizResultRepository
from domain.repositories.resource_favorite import BaseResourceFavoriteRepository
from domain.repositories.resource_image import BaseResourceImageRepository
from domain.repositories.resource_item import BaseResourceItemRepository
from domain.repositories.resource_rating import BaseResourceRatingRepository
from domain.repositories.user_account import BaseUserAccountRepository
from infrastructure.repositories.sql.category_item import SQLCategoryItemRepository
from infrastructure.repositories.sql.quiz_item import SQLQuizItemRepository
from infrastructure.repositories.sql.quiz_question import SQLQuizQuestionRepository
from infrastructure.repositories.sql.quiz_rating import SQLQuizRatingRepository
from infrastructure.repositories.sql.quiz_result import SQLQuizResultRepository
from infrastructure.repositories.sql.resource_favorite import SQLResourceFavoriteRepository
from infrastructure.repositories.sql.resource_image import SQLResourceImageRepository
from infrastructure.repositories.sql.resource_item import SQLResourceItemRepository
from infrastructure.repositories.sql.resource_rating import SQLResourceRatingRepository
from infrastructure.repositories.sql.user_account import SQLUserAccountRepository
from sqlalchemy.ext.asyncio import AsyncSession


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
