from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.base import Base


class QuizResultModel(Base):
    __tablename__ = "quiz_result"

    quiz_result_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)

    quiz_item_id: Mapped[PyUUID] = mapped_column(ForeignKey("quiz_item.quiz_item_id"))
    quiz_item: Mapped["QuizItemModel"] = relationship(back_populates="quiz_results")  # noqa: F821 # pyright: ignore

    user_account_id: Mapped[PyUUID] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["UserAccountModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_results",
    )

    percent: Mapped[int | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

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
