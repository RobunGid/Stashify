from datetime import datetime

from domain.enums import Role
from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.orm import relationship

from database.base import Base


class UserAccountModel(Base):
    __tablename__ = "user_account"

    user_id = Column(String, primary_key=True, default=str)
    username = Column(String)

    role = Column(Enum(Role))
    language = Column(String, nullable=False)

    connection_date = Column(DateTime, default=datetime.now)

    quiz_results = relationship("QuizResultModel", back_populates="user_account")
    quiz_ratings = relationship("QuizRatingModel", back_populates="user_account")
    resource_ratings = relationship("ResourceRatingModel", back_populates="user_account")
    resource_favorites = relationship("ResourceFavoriteModel", back_populates="user_account")
