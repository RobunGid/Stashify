from dataclasses import dataclass
from uuid import UUID

from domain.exceptions.base import ApplicationNotFoundException


@dataclass(eq=False)
class UserAccountNotFoundException(ApplicationNotFoundException):
    identifier: UUID | int | str

    @property
    def message(self):
        return "Requested user was not found; it may not exist or may have been removed"
