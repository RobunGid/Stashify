from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class ResourceModel(Base):
    __tablename__ = "resource"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    links = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    verified = Column(Boolean(), default=False, nullable=False)
    image = Column(String, nullable=False)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=False)
    category = relationship("CategoryModel", back_populates="resources")
    
    quiz = relationship("QuizModel", back_populates="resource", uselist=False)
    ratings = relationship("ResourceRatingModel", back_populates="resource", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    