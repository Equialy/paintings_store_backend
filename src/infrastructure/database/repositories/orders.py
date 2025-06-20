from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.orm import selectinload
from src.domain.orders.schemas.orders import OrderCreate, OrderRead, OrderStatus
from src.infrastructure.database.models.orders import Order, OrderItem
from src.infrastructure.database.models.pictures import Pictures


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
            stmt = sa.select(Pictures).where(Pictures.id == i.picture_id).with_for_update()
            db_picture = await self.session.execute(stmt)
            result_picture = db_picture.scalar_one()
            item_price = i.quantity * result_picture.price  # placeholder
            total += item_price
            result_picture.quantity -= 1
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
        await self.session.commit()
        result = await self.session.execute(
            sa.select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == db_order.id)
        )
        db_order = result.scalar_one()

        return OrderRead.model_validate(db_order)

    async def get_order_by_id(self, order_id: int) -> OrderRead:
        stmt = sa.select(self.model).where(self.model.id==order_id).options(selectinload(self.model.items))
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return OrderRead.model_validate(result)


    async def get_order_by_user_id(self, user_id: int, order_id: int) -> OrderRead:
        result = await self.session.execute(
            sa.select(self.model).where(self.model.id == order_id, self.model.user_id == user_id).options(
                selectinload(self.model.items))
        )
        db_order = result.scalars().one()
        return OrderRead.model_validate(db_order)

    async def list_orders(self) -> list[OrderRead]:
        stmt = sa.select(self.model).options(selectinload(self.model.items))
        execute = await self.session.execute(stmt)
        result = execute.scalars().all()
        return [OrderRead.model_validate(obj) for obj in result]



    async def list_orders_user(self, user_id: int) -> list[OrderRead]:
        result = await self.session.execute(
            sa.select(self.model).where(self.model.user_id == user_id).options(
                selectinload(self.model.items)).with_for_update()
        )
        db_order = result.scalars().all()
        return [OrderRead.model_validate(i) for i in db_order]

    async def update_status(self, order_id: int, status_order: OrderStatus) -> OrderRead:
        stmt = sa.update(Order).where(Order.id == order_id).values(status= status_order.value).options(
                selectinload(self.model.items)).returning(Order)
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return OrderRead.model_validate(result)
