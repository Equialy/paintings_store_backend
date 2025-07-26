from datetime import datetime
from sqlalchemy import Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.pictures import Pictures
from src.infrastructure.database.models.users import Users


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    picture_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pictures.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    added_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # связи
    user: Mapped["Users"] = relationship("Users", back_populates="cart_items")
    picture: Mapped["Pictures"] = relationship("Pictures")

    def __str__(self):
        return f"{self.id}"
