from dishka import provide, Provider, Scope

from application.services.quiz_item import QuizItemService
from application.services.quiz_rating import QuizRatingService
from application.services.resource_favorite import ResourceFavoriteService
from application.services.resource_item import ResourceItemService
from application.services.user_account import UserAccountService
from application.services.category_item import CategoryItemService
from application.services.quiz_question import QuizQuestionService
from application.services.quiz_result import QuizResultService
from application.services.resource_image import ResourceImageService
from application.services.resource_rating import ResourceRatingService

from infrastructure.repositories.quiz_item.base import BaseQuizItemRepository
from infrastructure.repositories.quiz_rating.base import BaseQuizRatingRepository
from infrastructure.repositories.resource_favorite.base import BaseResourceFavoriteRepository
from infrastructure.repositories.resource_item.base import BaseResourceItemRepository
from infrastructure.repositories.user_account.base import BaseUserAccountRepository
from infrastructure.repositories.category_item.base import BaseCategoryItemRepository
from infrastructure.repositories.quiz_question.base import BaseQuizQuestionRepository
from infrastructure.repositories.quiz_result.base import BaseQuizResultRepository
from infrastructure.repositories.resource_image.base import BaseResourceImageRepository
from infrastructure.repositories.resource_rating.base import BaseResourceRatingRepository


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_category_items_service(
        self,
        repository: BaseCategoryItemRepository,
    ) -> CategoryItemService:
        return CategoryItemService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_quiz_item_service(
        self,
        repository: BaseQuizItemRepository,
    ) -> QuizItemService:
        return QuizItemService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_quiz_rating_service(
        self,
        repository: BaseQuizRatingRepository,
    ) -> QuizRatingService:
        return QuizRatingService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_resource_favorite_service(
        self,
        repository: BaseResourceFavoriteRepository,
    ) -> ResourceFavoriteService:
        return ResourceFavoriteService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_resource_item_service(
        self,
        repository: BaseResourceItemRepository,
    ) -> ResourceItemService:
        return ResourceItemService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_user_account_service(
        self,
        repository: BaseUserAccountRepository,
    ) -> UserAccountService:
        return UserAccountService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_quiz_question_service(
        self,
        repository: BaseQuizQuestionRepository,
    ) -> QuizQuestionService:
        return QuizQuestionService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_quiz_result_service(
        self,
        repository: BaseQuizResultRepository,
    ) -> QuizResultService:
        return QuizResultService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_resource_image_service(
        self,
        repository: BaseResourceImageRepository,
    ) -> ResourceImageService:
        return ResourceImageService(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_resource_rating_service(
        self,
        repository: BaseResourceRatingRepository,
    ) -> ResourceRatingService:
        return ResourceRatingService(repository=repository)
