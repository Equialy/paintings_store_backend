from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.domain.orders.schemas.orders import OrderCreate, OrderRead
from src.infrastructure.database.models.orders import Order, OrderItem


class OrderRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Order

    async def create_order(self, user_id: int, order: OrderCreate) -> OrderRead:
        # calculate total
        total = 0
        items = []
        for i in order.items:
            # тут можно выбрать цену из БД
            item_price = i.quantity * 0  # placeholder
            total += item_price
            items.append(OrderItem(
                picture_id=i.picture_id,
                quantity=i.quantity,
                price=item_price
            ))
        db_order = Order(
            user_id=user_id,
            address=order.address,
            phone=order.phone,
            total=total,
            items=items
        )
        self.session.add(db_order)
        # await self.session.commit()
        await self.session.refresh(db_order)
        return OrderRead.model_validate(db_order)

    async def get_order(self, user_id: int, order_id: int) -> OrderRead:
        result = await self.session.execute(
            sa.select(self.model).where(self.model.id==order_id, self.model.user_id==user_id)
        )
        db_order = result.scalar_one()
        return OrderRead.model_validate(db_order)

    async def list_orders(self, user_id: int) -> list[OrderRead]:
        result = await self.session.execute(
            sa.select(self.model).where(self.model.user_id==user_id)
        )
        db_order = result.scalars().all()
        return [OrderRead.model_validate(i) for i in db_order ]

    async def update_status(self, order_id: int, status: str) -> OrderRead:
        execute = await self.session.execute(
            sa.update(Order).where(Order.id==order_id).values(status=status).returning(self.model))
        result = execute.scalar_one()
        return OrderRead.model_validate(result)
