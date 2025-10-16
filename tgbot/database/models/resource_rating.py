from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class ResourceRatingModel(Base):
    __tablename__ = "resource_rating"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'), nullable=False)
    resource = relationship("ResourceModel", back_populates="ratings")
    
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    user = relationship("UserModel", back_populates="resource_ratings")
    
    created_at = Column(DateTime, default=datetime.now)
    rating = Column(Integer)
    
    __table_args__ = (
			UniqueConstraint('user_id', 'resource_id', name='resource_rating_uix'),
			CheckConstraint('rating >= 1 AND rating <= 5',
					name='rating_boundaries'),
        )

    @validates('rating')
    def validate_rating(self, _, rating) -> int:
        if rating <= 0 or rating > 5:
            raise ValueError('Rating not in boundaries')
        return rating