from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class QuizItemModel(Base):
    __tablename__ = "quiz_item"

    quiz_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource_item.resource_item_id"),
        unique=True,
        nullable=False,
    )
    resource_item = relationship("ResourceItemModel", back_populates="quiz_item")

    quiz_questions = relationship(
        "QuizQuestionModel",
        back_populates="quiz_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    quiz_ratings = relationship("QuizRatingModel", back_populates="quiz_item")
    quiz_results = relationship("QuizResultModel", back_populates="quiz_item", lazy="dynamic")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
