from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.cart.interfaces.cart import CartRepositoryProtocol, CartServiceProtocol
from src.domain.cart.schemas.cart import CartItemPaginationResponse
from src.domain.cart.services.cart import CartServiceImpl
from src.infrastructure.database.base import get_async_session
from src.infrastructure.database.repositories.cart_repo import CartRepositoryImpl

# --- repositories ---

Session = Annotated[AsyncSession, Depends(get_async_session)]

def get_carts_repositories(session: Session) -> CartRepositoryProtocol:
    return CartRepositoryImpl(session)

CartFactoryRepository = Annotated[CartRepositoryProtocol, Depends(get_carts_repositories)]

# --- services ---

def get_carts_service(carts_factory_repositories: CartFactoryRepository) -> CartServiceProtocol:
    return CartServiceImpl(carts_factory_repositories)


CartsService = Annotated[CartServiceProtocol, Depends(get_carts_service)]

PaginationDep = Annotated[CartItemPaginationResponse,Depends(CartItemPaginationResponse)]