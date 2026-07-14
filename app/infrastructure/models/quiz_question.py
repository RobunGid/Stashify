from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class QuizQuestionModel(Base):
    __tablename__ = "quiz_question"

    quiz_question_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str]

    quiz_item_id: Mapped[PyUUID] = mapped_column(ForeignKey("quiz_item.quiz_item_id"))
    quiz_item: Mapped["QuizItemModel"] = relationship(back_populates="quiz_questions")  # noqa: F821 # pyright: ignore

    quiz_options: Mapped[list["QuizOptionModel"]] = relationship(  # noqa: F821 # pyright: ignore
        "QuizOptionModel",
        back_populates="quiz_question",
        cascade="all, delete-orphan",
    )
    image: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
