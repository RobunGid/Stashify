from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class CategoryItemModel(Base):
    __tablename__ = "category_item"

    category_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name = Column(String, unique=True, nullable=False)
    resource_items = relationship("ResourceItemModel", back_populates="category_item")
