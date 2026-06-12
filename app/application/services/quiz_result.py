from application.services.base import BaseService
from domain.entities.quiz_result import QuizResultEntity, QuizResultUpdateEntity
from domain.filters.quiz_result import QuizResultFilters


class QuizResultService(BaseService[QuizResultEntity, QuizResultUpdateEntity, QuizResultFilters]):
    pass
