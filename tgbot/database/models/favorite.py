from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.orm import Base

class FavoriteModel(Base):
    __tablename__ = "favorite"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'), nullable=False)
    
    added_at = Column(DateTime, default=datetime.now)
    user = relationship("UserModel", back_populates="favorites")
    resource = relationship("ResourceModel")