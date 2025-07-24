from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, Text, Numeric, ForeignKey, Integer
from sqlalchemy import DateTime, func

from src.infrastructure.database.base import Base


class Pictures(Base):
    """Картины: информация о названии, авторе, цене, наличии, категории."""

    __tablename__ = "pictures"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(
        Numeric(precision=18, scale=2), nullable=False, default=Decimal("0.00")
    )
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped["Categories"] = relationship(
        "Categories",
        back_populates="pictures",
    )

    __table_args__ = (CheckConstraint("quantity >= 0", name="quantity_non_negative"),)

    def __str__(self):
        return f"{self.title}"


class Categories(Base):
    """Категории картин (например: пейзажи, портреты, абстракции)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)

    pictures: Mapped[list[Pictures]] = relationship(
        "Pictures",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.title}"
