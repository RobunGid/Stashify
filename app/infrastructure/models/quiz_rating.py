from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from database.base import Base


class QuizRatingModel(Base):
    __tablename__ = "quiz_rating"

    quiz_rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    quiz_item_id = Column(UUID(as_uuid=True), ForeignKey("quiz_item.quiz_item_id"), nullable=False)
    quiz_item = relationship("QuizItemModel", back_populates="quiz_ratings")

    user_account_id = Column(UUID(as_uuid=True), ForeignKey("user_account.user_account_id"), nullable=False)
    user_account = relationship("UserAccountModel", back_populates="quiz_ratings")

    rating = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_account_id", "quiz_item_id", name="quiz_rating_uix"),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="rating_boundaries",
        ),
    )

    @validates("rating")
    def validate_rating(self, _, rating) -> int:
        if rating < 1 or rating > 5:
            raise ValueError("Rating not in boundaries")
        return rating
