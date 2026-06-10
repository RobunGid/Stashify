from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from database.orm import Base


class CategoryModel(Base):
    __tablename__ = "category"

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=UUID)

    name = Column(String, unique=True, nullable=False)
    resources = relationship("ResourceModel", back_populates="category")
