from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class QuizOptionModel(Base):
    __tablename__ = "quiz_option"

    quiz_option_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)

    quiz_question_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quiz_question.quiz_question_id"),
        nullable=False,
    )
    quiz_question: Mapped["CategoryItemModel"] = relationship(  # noqa: F821 # pyright: ignore
        "QuizQuestionModel",
        back_populates="quiz_options",
        lazy="joined",
    )

    text: Mapped[str]

    is_right: Mapped[bool] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
