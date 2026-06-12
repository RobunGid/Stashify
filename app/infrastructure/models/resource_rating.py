from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from database.base import Base


class ResourceRatingModel(Base):
    __tablename__ = "resource_rating"

    resource_rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource_item.resource_item_id"),
        nullable=False,
    )
    resource_item = relationship("ResourceItemModel", back_populates="resource_ratings")

    user_account_id = Column(UUID, ForeignKey("user_account.user_account_id"), nullable=False)
    user_account = relationship("UserAccountModel", back_populates="resource_ratings")

    rating = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_account_id", "resource_item_id", name="resource_rating_uix"),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="rating_boundaries",
        ),
    )

    @validates("rating")
    def validate_rating(self, _, rating) -> int:
        if rating <= 0 or rating > 5:
            raise ValueError("Rating not in boundaries")
        return rating
