from src.domain.orders.interfaces.orders import OrderRepositoryProtocol
from src.domain.orders.schemas.orders import (
    OrderCreate,
    OrderRead,
    OrderStatusUpdateSchema,
    OrderStatus,
)
from src.utils.payment_yookassa import yk_create


class OrderServiceImpl:
    def __init__(self, orders_factory_repository: OrderRepositoryProtocol):
        self.orders_factory_repository: OrderRepositoryProtocol = (
            orders_factory_repository
        )

    async def create_order(self, user_id: int, data: OrderCreate) -> OrderRead:
        order = await self.orders_factory_repository.create_order(user_id, data)
        confirmation_url, payment_id = await yk_create(
            amount="1", user_id=user_id  # или другой идентификатор
        )
        order = await self.orders_factory_repository.update_status(
            order.id,
            status_order=OrderStatus.PENDING,
            payment_id=payment_id,
            payment_url=confirmation_url,
        )
        return order

    async def get_order_by_user_id(self, user_id: int, order_id: int) -> OrderRead:
        return await self.orders_factory_repository.get_order_by_user_id(
            user_id, order_id
        )

    async def list_orders_user(self, user_id: int) -> list[OrderRead]:
        return await self.orders_factory_repository.list_orders_user(user_id)

    async def get_order_by_id(self, order_id: int) -> OrderRead:
        return await self.orders_factory_repository.get_order_by_id(order_id=order_id)

    async def list_orders(self) -> list[OrderRead]:
        return await self.orders_factory_repository.list_orders()

    async def update_status(
        self, order_id: int, status_order: OrderStatus
    ) -> OrderRead:
        return await self.orders_factory_repository.update_status(
            order_id, status_order
        )
