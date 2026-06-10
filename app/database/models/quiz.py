from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.orm import Base


class QuizModel(Base):
    __tablename__ = "quiz"

    quiz_id = Column(UUID(as_uuid=True), primary_key=True, default=UUID)

    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource.resource_item_id"),
        unique=True,
        nullable=False,
    )
    resource = relationship("ResourceModel", back_populates="quiz")

    questions = relationship(
        "QuizQuestionModel",
        back_populates="quiz",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    ratings = relationship("QuizRatingModel", back_populates="quiz")
    results = relationship("QuizResultModel", back_populates="quiz", lazy="dynamic")
