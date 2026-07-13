from abc import ABC

from domain.entities.quiz_option import QuizOptionEntity, QuizOptionUpdateEntity
from domain.filters.quiz_option import QuizOptionFilters
from domain.repositories.base import BaseRepository


class BaseQuizOptionRepository(
    BaseRepository[QuizOptionEntity, QuizOptionUpdateEntity, QuizOptionFilters],
    ABC,
):
    pass
