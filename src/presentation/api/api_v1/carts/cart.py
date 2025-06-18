from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.accounts.schemas.user import UsersSchemaAuth
from src.domain.cart.schemas.cart import CartItemRead, CartItemCreate, CartItemUpdate
from src.presentation.dependencies.authentication.user_dependecies import get_current_auth_user
from src.presentation.dependencies.carts.cart_di import CartsService
from src.settings import settings

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Cart"])

@router.get("/cart", response_model=list[CartItemRead])
async def read_cart(svc: CartsService, user: UsersSchemaAuth = Depends(get_current_auth_user)):
    return await svc.repo.get_cart(user.id)

@router.post("/cart", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
async def add_to_cart(item: CartItemCreate,svc: CartsService,
                      user: UsersSchemaAuth = Depends(get_current_auth_user),
                      ):
    pass
    # return await svc.add_to_cart(user.id, item)

@router.delete("/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(item_id: int,svc: CartsService,
                           user: UsersSchemaAuth = Depends(get_current_auth_user),
                           ):
    # await svc.repo.remove_item(user.id, item_id)
    pass


@router.patch(
    "/{item_id}",
    response_model=CartItemRead
)
async def update_cart_item(
    item_id: int,
    update: CartItemUpdate,
    service: CartsService ,
    user: UsersSchemaAuth = Depends(get_current_auth_user)
) -> CartItemRead:
    updated = await service.update_item(user.id, item_id, update.quantity)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return updated