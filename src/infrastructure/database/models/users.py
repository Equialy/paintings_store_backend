from datetime import datetime
from sqlalchemy import (
    Integer, String, Boolean, DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default='true', nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, server_default='false', nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Связь “один пользователь → много заказов”
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )
    # Связь “один пользователь → много элементов корзины”
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="user", cascade="all, delete-orphan"
    )
