from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, UniqueConstraint, String
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class QuizResultModel(Base):
    __tablename__ = "quiz_result"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    quiz_id = Column(UUID(as_uuid=True), ForeignKey('quiz.id'), nullable=False)
    quiz = relationship("QuizModel", back_populates="results")
    
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    user = relationship("UserModel", back_populates="quiz_results")
    
    completed_at = Column(DateTime, default=datetime.now)
    percent = Column(Integer)
    
    __table_args__ = (
			UniqueConstraint('user_id', 'quiz_id', name='quiz_result_uix_user_quiz'),
			CheckConstraint('percent >= 0 AND percent <= 100',
					name='percent_boundaries'),
        )

    @validates('percent')
    def validate_percent(self, _, percent) -> int:
        if percent < 0 or percent > 100:
            raise ValueError('Percent not in boundaries')
        return percent