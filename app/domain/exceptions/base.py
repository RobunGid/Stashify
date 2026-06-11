from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return "Unexpected error occurred in application while processing the request"


@dataclass(eq=False)
class ApplicationValidationException(ApplicationException):
    @property
    def message(self):
        return "Input data is invalid or does not match required format"


@dataclass(eq=False)
class ApplicationConflictException(ApplicationException):
    @property
    def message(self):
        return "Request conflicts with existing data; an entity with the same attributes already exists"


@dataclass(eq=False)
class ApplicationNotFoundException(ApplicationException):
    @property
    def message(self):
        return "Requested resource was not found; it may not exist or may have been removed"
