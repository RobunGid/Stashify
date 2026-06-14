from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.base import Base


class QuizRatingModel(Base):
    __tablename__ = "quiz_rating"

    quiz_rating_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    quiz_item_id: Mapped[UUID] = mapped_column(ForeignKey("quiz_item.quiz_item_id"))
    quiz_item: Mapped["QuizItemModel"] = relationship(back_populates="quiz_ratings")  # noqa: F821 # pyright: ignore

    user_account_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["UserAccountModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_ratings",
    )

    rating: Mapped[int | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

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
