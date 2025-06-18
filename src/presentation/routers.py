from fastapi import FastAPI
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

    return app
