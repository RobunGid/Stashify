from dataclasses import dataclass
from uuid import UUID

from domain.exceptions.base import ApplicationNotFoundException


@dataclass(eq=False)
class QuizItemNotFoundException(ApplicationNotFoundException):
    identifier: UUID | int | str

    @property
    def message(self):
        return "Requested quiz item was not found; it may not exist or may have been removed"
