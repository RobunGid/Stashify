from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class QuizItemModel(Base):
    __tablename__ = "quiz_item"

    quiz_item_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    resource_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("resource_item.resource_item_id"),
        unique=True,
    )
    resource_item: Mapped["ResourceItemModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_item",
    )

    quiz_questions: Mapped[list["QuizQuestionModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    quiz_ratings: Mapped[list["QuizRatingModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_item",
    )
    quiz_results: Mapped[list["QuizResultModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="quiz_item",
        lazy="dynamic",
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
