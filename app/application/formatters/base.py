from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseFormatter(
    ABC,
):
    pass


@dataclass
class BaseDateFormatter(BaseFormatter):
    pattern: str

    def format_date(self, dt: datetime) -> str:
        return dt.strftime(self.pattern)


@dataclass
class DefaultDateFormatter(BaseDateFormatter):
    pattern: str = "%d.%m.%Y %H:%M"


@dataclass
class BaseVerifiedStatusFormatter(BaseFormatter):
    @abstractmethod
    def format_status(self, is_verified: bool) -> str:
        pass


@dataclass
class BaseTranslateContextBuilder(ABC):
    @abstractmethod
    def build(self) -> dict:
        pass
