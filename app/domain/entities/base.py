from abc import ABC
from dataclasses import field
from datetime import datetime


class BaseEntity(ABC):
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)
