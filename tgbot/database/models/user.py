from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from database.orm import Base

class UserModel(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tg_id = Column(String, unique=True)
    
    connection_date = Column(DateTime, default=datetime.now)