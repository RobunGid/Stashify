from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class QuizRatingModel(Base):
    __tablename__ = "quiz_rating"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    quiz_id = Column(UUID(as_uuid=True), ForeignKey('quiz.id'), nullable=False)
    quiz = relationship("QuizModel", back_populates="ratings")
    
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    user = relationship("UserModel", back_populates="quiz_ratings")
    
    created_at = Column(DateTime, default=datetime.now)
    rating = Column(Integer)
    
    __table_args__ = (
			UniqueConstraint('user_id', 'quiz_id', name='quiz_rating_uix'),
			CheckConstraint('rating >= 1 AND rating <= 5',
					name='rating_boundaries'),
        )

    @validates('rating')
    def validate_rating(self, _, rating) -> int:
        if rating <= 0 or rating > 5:
            raise ValueError('Rating not in boundaries')
        return rating