from datetime import datetime
from uuid import uuid4

from domain.entities.category_item import CategoryItemEntity
from sqlalchemy import DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class CategoryItemModel(Base):
    __tablename__ = "category_item"

    category_item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    resource_items: Mapped[list["ResourceItemModel"]] = relationship(  # noqa: F821 # pyright: ignore
        "ResourceItemModel",
        back_populates="category_item",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def from_entity(cls, entity: CategoryItemEntity):
        return cls(
            category_item_id=entity.category_item_id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
