from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, func
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class ResourceImageModel(Base):
    __tablename__ = "resource_image"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'), nullable=False)
    resource = relationship("ResourceModel", back_populates="ratings")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    image = Column(String, nullable=False)