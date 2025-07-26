from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.orders.schemas.orders import OrderStatus
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.pictures import Pictures


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=OrderStatus.PENDING
    )
    total: Mapped[Numeric] = mapped_column(Numeric(18, 2), nullable=False)
    payment_id = mapped_column(String, nullable=True)
    payment_url = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    user = relationship("Users", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    picture_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pictures.id", ondelete="SET NULL"), nullable=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(18, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    picture: Mapped["Pictures"] = relationship("Pictures")

    def __str__(self):
        return f"{self.id}"
