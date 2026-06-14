from datetime import datetime
from uuid import uuid4

from infrastructure.models.resource_item import ResourceItemModel
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class ResourceImageModel(Base):
    __tablename__ = "resource_image"

    resource_image_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    resource_item_id: Mapped[UUID] = mapped_column(ForeignKey("resource_item.resource_item_id"))
    resource_item: Mapped[ResourceItemModel] = relationship(back_populates="resource_images")

    image: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
