from application.services.base import BaseService
from domain.entities.quiz_rating import QuizRatingEntity, QuizRatingUpdateEntity
from domain.filters.quiz_rating import QuizRatingFilters


class QuizItemService(BaseService[QuizRatingEntity, QuizRatingUpdateEntity, QuizRatingFilters]):
    pass
