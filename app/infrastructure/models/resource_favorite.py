from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class ResourceFavoriteModel(Base):
    __tablename__ = "resource_favorite"

    resource_favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_account_id = Column(UUID(as_uuid=True), ForeignKey("user_account.user_account_id"), nullable=False)
    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource_item.resource_item_id"),
        nullable=False,
    )

    added_at = Column(DateTime, default=datetime.now)
    user_account = relationship("UserAccountModel", back_populates="resource_favorites")
    resource_item = relationship("ResourceItemModel")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
