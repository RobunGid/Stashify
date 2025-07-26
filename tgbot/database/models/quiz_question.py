from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from database.orm import Base

class QuizQuestionModel(Base):
    __tablename__ = "quiz_question"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    quiz_id = Column(UUID(as_uuid=True), ForeignKey('quiz.id'), nullable=False)
    quiz = relationship("QuizModel", back_populates="questions")
    
    options = Column(ARRAY(String), nullable=False)
    answer = Column(String(), nullable=False)

    