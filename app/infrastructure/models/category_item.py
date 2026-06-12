from uuid import uuid4

from domain.entities.category_item import CategoryItemEntity
from sqlalchemy import Column, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class CategoryItemModel(Base):
    __tablename__ = "category_item"

    category_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name = Column(String, unique=True, nullable=False)
    resource_items = relationship("ResourceItemModel", back_populates="category_item")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def from_entity(cls, entity: CategoryItemEntity):
        return cls(
            category_item_id=entity.category_item_id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
