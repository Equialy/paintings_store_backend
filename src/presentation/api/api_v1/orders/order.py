from fastapi import APIRouter, Depends, status
from typing import List

from src.domain.accounts.schemas.user import UsersSchemaAuth
from src.domain.orders.schemas.orders import OrderCreate, OrderRead
from src.presentation.dependencies.authentication.user_dependecies import get_current_auth_user
from src.presentation.dependencies.orders.order_di import OrderService
from src.settings import settings

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Orders"])

@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    svc: OrderService ,
    user: UsersSchemaAuth = Depends(get_current_auth_user)
):
    return await svc.create_order(user.id, data)

@router.get("/orders", response_model=List[OrderRead])
async def list_orders(
    svc: OrderService ,
    user: UsersSchemaAuth = Depends(get_current_auth_user)
):
    return await svc.list_orders(user.id)

@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    svc: OrderService ,
    user: UsersSchemaAuth = Depends(get_current_auth_user)
):
    return await svc.get_order(user.id, order_id)

@router.patch("/orders/{order_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_status(
    order_id: int,
    status: str,
    svc: OrderService ,
):
    await svc.update_status(order_id, status)
