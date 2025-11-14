from uuid import uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class QuizModel(Base):
    __tablename__ = "quiz"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'), unique=True, nullable=False)
    resource = relationship("ResourceModel", back_populates="quiz")
    
    questions = relationship("QuizQuestionModel", back_populates="quiz", cascade="all, delete-orphan", lazy="joined")
    ratings = relationship("QuizRatingModel", back_populates="quiz")
    results = relationship("QuizResultModel", back_populates="quiz", lazy="dynamic")