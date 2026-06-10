from datetime import datetime

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

from database.orm import Base


class QuizRatingModel(Base):
    __tablename__ = "quiz_rating"

    quiz_rating_id = Column(UUID(as_uuid=True), primary_key=True, default=UUID)

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.quiz_id"), nullable=False)
    quiz = relationship("QuizModel", back_populates="ratings")

    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    user = relationship("UserModel", back_populates="quiz_ratings")

    created_at = Column(DateTime, default=datetime.now)
    rating = Column(Integer)

    __table_args__ = (
        UniqueConstraint("user_id", "quiz_id", name="quiz_rating_uix"),
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
