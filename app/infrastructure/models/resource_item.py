from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class ResourceItemModel(Base):
    __tablename__ = "resource_item"

    resource_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    telegram_id = Column(Integer)

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    links = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    verified = Column(Boolean(), default=False, nullable=False)

    category_item_id = Column(UUID(as_uuid=True), ForeignKey("category_item.category_item_id"), nullable=False)
    category_item = relationship("CategoryItemModel", back_populates="resource_items", lazy="joined")

    quiz_item = relationship(
        "QuizItemModel",
        back_populates="resource_item",
        uselist=False,
        lazy="joined",
    )
    resource_ratings = relationship(
        "ResourceRatingModel",
        back_populates="resource_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    resource_images = relationship(
        "ResourceImageModel",
        back_populates="resource_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
