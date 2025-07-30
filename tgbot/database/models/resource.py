from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class ResourceModel(Base):
    __tablename__ = "resource"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    name = Column(String, unique=True)
    description = Column(String, unique=True)
    tags = Column(String, unique=True)
    verified = Column(Boolean(), default=False)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    category = relationship("CategoryModel", back_populates="resources")
    
    quizes = relationship("QuizModel", back_populates="resource")
    
    created_at = Column(DateTime, default=datetime.now)
    