from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.orm import Base


class ResourceImageModel(Base):
    __tablename__ = "resource_image"

    resource_image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    resource_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resource_item.resource_item_id"),
        nullable=False,
    )
    resource_item = relationship("ResourceItemModel", back_populates="images")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    image = Column(String, nullable=False)
