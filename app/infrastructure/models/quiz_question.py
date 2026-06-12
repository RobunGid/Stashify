from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from database.base import Base


class QuizQuestionModel(Base):
    __tablename__ = "quiz_question"

    quiz_question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)

    quiz_item_id = Column(UUID(as_uuid=True), ForeignKey("quiz_item.quiz_item_id"), nullable=False)
    quiz_item = relationship("QuizItemModel", back_populates="quiz_questions")

    options = Column(ARRAY(String), nullable=False)
    right_options = Column(ARRAY(Integer), nullable=False)

    image = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
