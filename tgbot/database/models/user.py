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
    
    id = Column(String, primary_key=True, default=str)
    username = Column(String)
    
    role = Column(Enum(Role))
    language = Column(String, nullable=False)
    
    connection_date = Column(DateTime, default=datetime.now)
    
    quiz_results = relationship("QuizResultModel", back_populates="user")
    quiz_ratings = relationship("QuizRatingModel", back_populates="user")
    favorites = relationship("FavoriteModel", back_populates="user")
    