from typing import Protocol, List

from src.domain.orders.schemas.orders import (
    OrderRead,
    OrderCreate,
    OrderStatusUpdateSchema,
    OrderStatus,
)


class OrderRepositoryProtocol(Protocol):
    async def create_order(self, user_id: int, order: OrderCreate) -> OrderRead: ...

    async def get_order_by_user_id(self, user_id: int, order_id: int) -> OrderRead: ...

    async def list_orders_user(self, user_id: int) -> List[OrderRead]: ...

    async def update_status(
        self,
        order_id: int,
        status_order: OrderStatus,
        payment_id: str,
        payment_url: str,
    ) -> OrderRead: ...

    async def list_orders(self) -> List[OrderRead]: ...

    async def get_order_by_id(self, order_id: int) -> OrderRead: ...

    async def update_payment_info(
        self, order_id: int, payment_id: str, payment_url: str
    ) -> OrderRead: ...


class OrderServiceProtocol(Protocol):

    async def create_order(self, user_id: int, data: OrderCreate) -> OrderRead: ...

    async def get_order_by_user_id(self, user_id: int, order_id: int) -> OrderRead: ...

    async def list_orders_user(self, user_id: int) -> list[OrderRead]: ...

    async def update_status(
        self, order_id: int, status_order: OrderStatus
    ) -> OrderRead: ...

    async def list_orders(self) -> List[OrderRead]: ...

    async def get_order_by_id(self, order_id: int) -> OrderRead: ...
