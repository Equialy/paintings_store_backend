from fastapi import FastAPI

from sqladmin import Admin

from src.domain.admin.services.admin import (
    UserAdmin,
    PictureAdmin,
    CategoryAdmin,
    OrdersAdmin,
    CartItemAdmin,
    OrderItemAdmin,
)
from src.domain.admin.services.auth import authentication_backend
from src.infrastructure.database.base import asyncio_engine
from src.presentation.api.api_v1.pictures.routers import router as picture_router
from src.presentation.api.api_v1.users.auth import router as auth_router
from src.presentation.api.api_v1.carts.cart import router as carts_router
from src.presentation.api.api_v1.orders.order import router as order_router
from src.presentation.api.api_v1.admin.admin_pictures import router as admin_router


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(admin_router)
    app.include_router(carts_router)
    app.include_router(order_router)
    app.include_router(picture_router)
    app.include_router(auth_router)
    admin = Admin(app, asyncio_engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(PictureAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(OrdersAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(OrderItemAdmin)

    return app
