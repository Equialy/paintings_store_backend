from fastapi import APIRouter, Depends, status

from src.domain.accounts.schemas.user import UsersSchemaAuth
from src.domain.orders.schemas.orders import (
    OrderCreate,
    OrderRead,
)
from src.presentation.dependencies.authentication.user_dependecies import (
    get_current_auth_user,
)
from src.presentation.dependencies.orders.order_di import OrderService
from src.settings import settings

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Orders"])


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    svc: OrderService,
    user: UsersSchemaAuth = Depends(get_current_auth_user),
) -> OrderRead:
    return await svc.create_order(user.id, data)


@router.get("/orders", response_model=list[OrderRead])
async def list_orders(
    svc: OrderService, user: UsersSchemaAuth = Depends(get_current_auth_user)
):
    return await svc.list_orders_user(user.id)


@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    svc: OrderService,
    user: UsersSchemaAuth = Depends(get_current_auth_user),
) -> OrderRead:
    return await svc.get_order_by_user_id(user.id, order_id)
