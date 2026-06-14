from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.base import Base


class ResourceRatingModel(Base):
    __tablename__ = "resource_rating"

    resource_rating_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    resource_item_id: Mapped[UUID] = mapped_column(ForeignKey("resource_item.resource_item_id"))
    resource_item: Mapped["ResourceItemModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="resource_ratings",
    )

    user_account_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["UserAccountModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="resource_ratings",
    )

    rating: Mapped[int | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint("user_account_id", "resource_item_id", name="resource_rating_uix"),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="rating_boundaries",
        ),
    )

    @validates("rating")
    def validate_rating(self, _, rating) -> int:
        if rating <= 0 or rating > 5:
            raise ValueError("Rating not in boundaries")
        return rating
