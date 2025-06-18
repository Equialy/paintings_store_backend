from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.orders.interfaces.orders import OrderRepositoryProtocol, OrderServiceProtocol
from src.domain.orders.services.cart_use_case import OrderServiceImpl
from src.infrastructure.database.base import get_async_session
from src.infrastructure.database.repositories.orders import OrderRepositoryImpl

# --- repositories ---

Session = Annotated[AsyncSession, Depends(get_async_session)]

def get_orders_repositories(session: Session) -> OrderRepositoryProtocol:
    return OrderRepositoryImpl(session)

OrderFactoryRepository = Annotated[OrderRepositoryProtocol, Depends(get_orders_repositories)]

# --- services ---

def get_orders_service(order_factory_repositories: OrderFactoryRepository) -> OrderServiceProtocol:
    return OrderServiceImpl(order_factory_repositories)


OrderService = Annotated[OrderServiceProtocol, Depends(get_orders_service)]

