from abc import ABC

from domain.entities.quiz_question import QuizQuestionEntity, QuizQuestionUpdateEntity
from domain.filters.quiz_question import QuizQuestionFilters
from infrastructure.repositories.base import BaseRepository


class BaseQuizQuestionRepository(
    BaseRepository[QuizQuestionEntity, QuizQuestionUpdateEntity, QuizQuestionFilters],
    ABC,
):
    pass
