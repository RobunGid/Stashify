from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from domain.entities.user_account import Role
from sqlalchemy import BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class UserAccountModel(Base):
    __tablename__ = "user_account"

    user_account_id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None]

    role: Mapped[Role | None] = mapped_column(Enum(Role))

    quiz_results: Mapped[list["QuizResultModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="user_account",
    )
    quiz_ratings: Mapped[list["QuizRatingModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="user_account",
    )
    resource_ratings: Mapped[list["ResourceRatingModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="user_account",
    )
    resource_favorites: Mapped[list["ResourceFavoriteModel"]] = relationship(  # noqa: F821 # pyright: ignore
        back_populates="user_account",
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
