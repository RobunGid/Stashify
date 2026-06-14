from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class QuizQuestionModel(Base):
    __tablename__ = "quiz_question"

    quiz_question_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str]

    quiz_item_id: Mapped[PyUUID] = mapped_column(ForeignKey("quiz_item.quiz_item_id"))
    quiz_item: Mapped["QuizItemModel"] = relationship(back_populates="quiz_questions")  # noqa: F821 # pyright: ignore

    options: Mapped[list[str]] = mapped_column(ARRAY(String))
    right_options: Mapped[list[int]] = mapped_column(ARRAY(String))
    index: Mapped[int]

    image: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    __table_args__ = (UniqueConstraint("quiz_item_id", "index", name="uq_quiz_question_item_index"),)
