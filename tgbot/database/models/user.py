from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.orm import Base

class Role(PyEnum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'

class UserModel(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tg_id = Column(String, unique=True)
    
    role = Column(Enum(Role))
    
    connection_date = Column(DateTime, default=datetime.now)
    
    quiz_results = relationship("QuizResultModel", back_populates="user")
    quiz_ratings = relationship("QuizRatingModel", back_populates="user")
    