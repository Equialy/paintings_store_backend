from src.domain.orders.interfaces.orders import OrderRepositoryProtocol
from src.domain.orders.schemas.orders import OrderCreate, OrderRead


class OrderServiceImpl:
    def __init__(self, orders_factory_repository: OrderRepositoryProtocol):
        self.orders_factory_repository = orders_factory_repository

    async def create_order(self, user_id: int, data: OrderCreate) -> OrderRead:
        return await self.orders_factory_repository.create_order(user_id, data)

    async def get_order(self, user_id: int, order_id: int) -> OrderRead:
        return await self.orders_factory_repository.get_order(user_id, order_id)

    async def list_orders(self, user_id: int) -> list[OrderRead]:
        return await self.orders_factory_repository.list_orders(user_id)

    async def update_status(self, order_id: int, status: str) -> None:
        await self.orders_factory_repository.update_status(order_id, status)