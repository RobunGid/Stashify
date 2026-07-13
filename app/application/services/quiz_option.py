from dataclasses import dataclass

from application.services.base import BaseService
from domain.entities.quiz_option import QuizOptionEntity, QuizOptionUpdateEntity
from domain.filters.quiz_option import QuizOptionFilters
from domain.repositories.quiz_option import BaseQuizOptionRepository


@dataclass
class QuizOptionService(BaseService[QuizOptionEntity, QuizOptionUpdateEntity, QuizOptionFilters]):
    repository: BaseQuizOptionRepository
