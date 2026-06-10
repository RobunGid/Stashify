from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from database.orm import Base


class ResourceRatingModel(Base):
    __tablename__ = "resource_rating"

    resource_rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource_item.resource_item_id"),
        nullable=False,
    )
    resource_item = relationship("ResourceItemModel", back_populates="ratings")

    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    user = relationship("UserModel", back_populates="resource_ratings")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    rating = Column(Integer)

    __table_args__ = (
        UniqueConstraint("user_id", "resource_item_id", name="resource_rating_uix"),
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
