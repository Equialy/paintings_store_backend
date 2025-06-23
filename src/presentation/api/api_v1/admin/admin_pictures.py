import logging

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile

from src.domain.accounts.schemas.user import UsersSchemaAuth
from src.domain.orders.schemas.orders import (
    OrderRead,
    OrderStatus,
)
from src.domain.pictures.schemas.pictures import (
    PictureReadSchema,
    PictureUpdateSchema,
    PictureCreateSchema,
    CategoryCreate,
    CategoryRead,
)
from src.presentation.dependencies.admin.admin_di import get_current_admin_user
from src.presentation.dependencies.orders.order_di import OrderService
from src.presentation.dependencies.pictures.services import PicturesService
from src.settings import settings
from src.utils.storage import save_upload_file

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Admin"])
logger = logging.getLogger(__name__)


@router.get("/admin/orders", response_model=list[OrderRead])
async def list_all_orders(
    service: OrderService, user: UsersSchemaAuth = Depends(get_current_admin_user)
) -> list[OrderRead]:
    return await service.list_orders()


@router.get("/admin/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    service: OrderService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> OrderRead:
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    update: OrderStatus,
    service: OrderService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> OrderRead:
    return await service.update_status(order_id=order_id, status_order=update)


@router.post("/admin/pictures/category", response_model=CategoryRead)
async def add_category(
    category: CategoryCreate,
    picture_service: PicturesService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> CategoryRead:
    return await picture_service.create_category(schema=category)


@router.get("/admin/pictures/category", response_model=list[CategoryRead])
async def get_all_category(
    picture_service: PicturesService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> list[CategoryRead]:
    return await picture_service.get_all_category()


@router.post("/admin/pictures", response_model=PictureReadSchema)
async def add_picture(
    picture: PictureCreateSchema,
    picture_service: PicturesService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> PictureReadSchema:
    return await picture_service.create_picture(schema=picture)


@router.put("/admin/pictures/{picture_id}", response_model=PictureReadSchema)
async def update_picture(
    picture: PictureUpdateSchema,
    picture_service: PicturesService,
    file: UploadFile,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> PictureReadSchema:
    file_path = await save_upload_file(file)
    return await picture_service.update_picture(picture_id=picture)


@router.patch("/admin/pictures/{picture_id}", response_model=PictureReadSchema)
async def patch_picture(
    # picture: PictureUpdateSchema,
    picture_service: PicturesService,
    picture_id: int,
    file: UploadFile,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> PictureReadSchema:
    file_path = await save_upload_file(file)
    logger.info("формирование url %s", file_path)
    return await picture_service.patch_picture(
        file_path=file_path, picture_id=picture_id
    )


@router.delete("/admin/pictures/{picture_id}", response_model=PictureReadSchema)
async def delete_picture(
    picture_id: int,
    picture_service: PicturesService,
    user: UsersSchemaAuth = Depends(get_current_admin_user),
) -> PictureReadSchema:
    return await picture_service.delete_book(book_id=picture_id)
