from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from database.orm import Base


class QuizQuestionModel(Base):
    __tablename__ = "quiz_question"

    quiz_question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.quiz_id"), nullable=False)
    quiz = relationship("QuizModel", back_populates="questions")

    options = Column(ARRAY(String), nullable=False)
    right_options = Column(ARRAY(Integer), nullable=False)

    image = Column(String)
