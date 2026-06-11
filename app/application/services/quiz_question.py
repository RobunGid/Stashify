from application.services.base import BaseService
from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters


class QuizQuestionService(BaseService[QuizQuestionEntity, QuizQuestionUpdateEntity, QuizQuestionFilters]):
    pass
