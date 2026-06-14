from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class ResourceFavoriteModel(Base):
    __tablename__ = "resource_favorite"

    resource_favorite_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)

    user_account_id: Mapped[PyUUID] = mapped_column(ForeignKey("user_account.user_account_id"))
    resource_item_id: Mapped[PyUUID] = mapped_column(ForeignKey("resource_item.resource_item_id"))

    added_at: Mapped[datetime] = mapped_column(default=datetime.now)

    user_account: Mapped["UserAccountModel"] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="resource_favorites",
    )
    resource_item: Mapped["ResourceItemModel"] = relationship()  # noqa: F821 # pyright: ignore

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
