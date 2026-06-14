from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class ResourceItemModel(Base):
    __tablename__ = "resource_item"

    resource_item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[str] = mapped_column(String, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    category_item_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("category_item.category_item_id"),
        nullable=False,
    )

    category_item: Mapped["CategoryItemModel"] = relationship(  # noqa: F821 # pyright: ignore
        "CategoryItemModel",
        back_populates="resource_items",
        lazy="joined",
    )

    quiz_item: Mapped["QuizItemModel"] = relationship(  # noqa: F821 # pyright: ignore
        "QuizItemModel",
        back_populates="resource_item",
        uselist=False,
        lazy="joined",
    )

    resource_ratings: Mapped[list["ResourceRatingModel"]] = relationship(  # noqa: F821 # pyright: ignore
        "ResourceRatingModel",
        back_populates="resource_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    resource_images: Mapped[list["ResourceImageModel"]] = relationship(  # noqa: F821 # pyright: ignore
        "ResourceImageModel",
        back_populates="resource_item",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
