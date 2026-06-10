from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

from database.orm import Base


class FavoriteModel(Base):
    __tablename__ = "favorite"

    favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=UUID)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    resource_item_id = Column(UUID(as_uuid=True), ForeignKey("resource.resource_item_id"), nullable=False)

    added_at = Column(DateTime, default=datetime.now)
    user = relationship("UserModel", back_populates="favorites")
    resource = relationship("ResourceModel")
