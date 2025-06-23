from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.cart.schemas.cart import (
    CartItemRead,
    CartItemCreate,
    CartItemSchema,
    CartItemUpdate,
)
from src.infrastructure.database.models.cart_item import CartItem
from sqlalchemy.orm import selectinload

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

    async def add(self, user_id: int, item: CartItemCreate) -> CartItemSchema:
        stmt = (
            sa.insert(self.model)
            .values(user_id=user_id, **item.model_dump())
            .options(selectinload(self.model.picture))
            .returning(self.model)
        )
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return CartItemSchema.model_validate(
            {
                "id": result.id,
                "picture_id": result.picture_id,
                "quantity": result.quantity,
                "picture": {
                    "id": result.picture.id,
                    "price": float(result.picture.price),
                    "title": result.picture.title,
                },
            }
        )

    async def remove_item(self, item_id: int, user_id: int) -> CartItemSchema:
        stmt = (
            sa.delete(self.model)
            .where(self.model.id == item_id, self.model.user_id == user_id)
            .options(selectinload(self.model.picture))
            .returning(self.model)
        )
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return CartItemSchema.model_validate(result)

    async def update_item(
        self, user_id: int, item_id: int, update: CartItemUpdate
    ) -> CartItemRead:
        stmt = (
            sa.update(self.model)
            .where(
                self.model.id == item_id,
                self.model.user_id == user_id,
            )
            .values(quantity=update.quantity)
            .returning(self.model)
        )
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return CartItemRead.model_validate(result)

    async def clear_cart(self, user_id: int) -> CartItemRead:
        stmt = (
            sa.delete(self.model)
            .where(self.model.user_id == user_id)
            .returning(self.model)
        )
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return CartItemRead.model_validate(result)
