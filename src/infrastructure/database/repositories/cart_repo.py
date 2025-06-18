from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.cart.schemas.cart import CartItemRead
from src.infrastructure.database.models.cart_item import CartItem

import sqlalchemy as sa

class CartRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = CartItem

    async def get_cart(self, user_id: int) -> list[CartItemRead]:
        result = await self.session.execute(
            sa.select(self.model).where(self.model.user_id == user_id)
        )
        items = result.scalars().all()
        return [CartItemRead.model_validate(i) for i in items]

    # TODO: add_item, remove_item, update_item, clear_cart
