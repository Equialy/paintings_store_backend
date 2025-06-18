from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.accounts.schemas.user import UsersSchemaAuth
from src.domain.orders.schemas.orders import OrderRead, OrderStatusUpdateSchema
from src.domain.pictures.schemas.pictures import PictureReadSchema, PictureUpdateSchema, PictureCreateSchema
from src.presentation.dependencies.admin.admin_di import get_current_admin_user
from src.presentation.dependencies.orders.order_di import OrderService
from src.presentation.dependencies.pictures.services import PicturesService
from src.settings import settings

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Admin"])


@router.get("/admin/orders", response_model=list[OrderRead])
async def list_all_orders(service: OrderService,
                          user: UsersSchemaAuth = Depends(get_current_admin_user)) -> list[OrderRead]:
    return await service.list_orders(user_id=None)


@router.get("/admin/orders/{order_id}", response_model=OrderRead)
async def get_order(
        order_id: int,
        service: OrderService,
        user: UsersSchemaAuth = Depends(get_current_admin_user)
) -> OrderRead:
    order = await service.get_order(user_id=None, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_order_status(
        order_id: int,
        update: OrderStatusUpdateSchema,
        service: OrderService,
        user: UsersSchemaAuth = Depends(get_current_admin_user)
):
    _ = await service.get_order(user_id=None, order_id=order_id)
    await service.update_status(order_id=order_id, status=update.status)


@router.post("/admin/pictures", response_model=PictureReadSchema)
async def add_picture(picture: PictureCreateSchema, picture_service: PicturesService,
                      user: UsersSchemaAuth = Depends(get_current_admin_user)) -> PictureReadSchema:
    return await picture_service.create_picture(schema=picture)


@router.put("/admin/pictures/{book_id}", response_model=PictureReadSchema)
async def update_picture(picture: PictureUpdateSchema, picture_service: PicturesService,
                         user: UsersSchemaAuth = Depends(get_current_admin_user)) -> PictureReadSchema:
    return await picture_service.update_picture(picture_id=picture)


@router.delete("/admin/pictures/{book_id}", response_model=PictureReadSchema)
async def delete_picture(picture_id: int, picture_service: PicturesService,
                         user: UsersSchemaAuth = Depends(get_current_admin_user)) -> PictureReadSchema:
    return await picture_service.delete_book(book_id=picture_id)
