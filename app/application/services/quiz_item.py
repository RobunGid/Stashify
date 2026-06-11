from application.services.base import BaseService
from domain.entities.quiz_item import QuizItemEntity, QuizItemUpdateEntity
from domain.filters.quiz_item import QuizItemFilters


class QuizItemService(BaseService[QuizItemEntity, QuizItemUpdateEntity, QuizItemFilters]):
    pass
