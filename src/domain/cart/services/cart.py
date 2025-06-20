from src.domain.cart.interfaces.cart import CartRepositoryProtocol
from src.domain.cart.schemas.cart import CartItemPaginationResponse, CartItemSchema, CartItemRead, CartItemCreate, \
    CartItemUpdate


class CartServiceImpl:
    def __init__(self, cart_factory_repository: CartRepositoryProtocol):
        self.cart_factory_repository = cart_factory_repository

    async def get_cart_by_user(self, user_id: int) -> list[CartItemRead]:
        return await self.cart_factory_repository.get_cart(user_id=user_id)

    async def add_cart(self, user_id: int, item: CartItemCreate) -> CartItemSchema:
        return await self.cart_factory_repository.add(user_id=user_id, item=item)

    async def update_cart(self,user_id: int, item_id: int, update: CartItemUpdate) -> CartItemRead:
        return await self.cart_factory_repository.update_item(user_id=user_id, item_id=item_id, update=update)

    async def remove_cart(self, item_id: int, user_id: int) -> CartItemSchema:
        return await self.cart_factory_repository.remove_item(item_id=item_id, user_id=user_id)

    async def clear_cart_service(self, user_id: int) -> CartItemRead:
        return await self.cart_factory_repository.clear_cart(user_id=user_id)

