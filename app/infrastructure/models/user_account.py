from uuid import uuid4

from domain.enums import Role
from sqlalchemy import BigInteger, Column, DateTime, Enum, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class UserAccountModel(Base):
    __tablename__ = "user_account"

    user_account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_telegram_id = Column(BigInteger)
    username = Column(String)

    role = Column(Enum(Role))

    quiz_results = relationship("QuizResultModel", back_populates="user_account")
    quiz_ratings = relationship("QuizRatingModel", back_populates="user_account")
    resource_ratings = relationship("ResourceRatingModel", back_populates="user_account")
    resource_favorites = relationship("ResourceFavoriteModel", back_populates="user_account")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
