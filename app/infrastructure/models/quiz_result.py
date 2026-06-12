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


class QuizResultModel(Base):
    __tablename__ = "quiz_result"

    quiz_result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    quiz_item_id = Column(UUID(as_uuid=True), ForeignKey("quiz_item.quiz_item_id"), nullable=False)
    quiz_item = relationship("QuizItemModel", back_populates="quiz_results")

    user_account_id = Column(UUID, ForeignKey("user_account.user_account_id"), nullable=False)
    user_account = relationship("UserAccountModel", back_populates="quiz_results")

    percent = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_account_id", "quiz_item_id", name="quiz_result_uix_user_quiz"),
        CheckConstraint(
            "percent >= 0 AND percent <= 100",
            name="percent_boundaries",
        ),
    )

    @validates("percent")
    def validate_percent(self, _, percent) -> int:
        if percent < 0 or percent > 100:
            raise ValueError("Percent not in boundaries")
        return percent
