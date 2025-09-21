from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class FavoriteModel(Base):
    __tablename__ = "favorite"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tg_id = Column(String, ForeignKey('user.tg_id'), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'), nullable=False)
    
    added_date = Column(DateTime, default=datetime.now)