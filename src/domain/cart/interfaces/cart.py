from typing import Protocol

from src.domain.cart.schemas.cart import CartItemSchema, CartItemPaginationResponse, CartItemRead, CartItemCreate, \
    CartItemUpdate


class CartRepositoryProtocol(Protocol):

    async def add(self, user_id: int, item: CartItemCreate) -> CartItemSchema: ...

    async def get_cart(self, user_id: int) ->list[CartItemRead]: ...\

    async def update_item(self,user_id: int,  item_id: int, update: CartItemUpdate) -> CartItemRead: ...

    async def remove_item(self, item_id: int, user_id: int) -> CartItemSchema: ...

    async def clear_cart(self, user_id: int) -> CartItemRead: ...



class CartServiceProtocol(Protocol):

    async def add_cart(self, user_id: int, item: CartItemCreate) -> CartItemSchema: ...

    async def get_cart_by_user(self, user_id: int) ->list[CartItemRead]: ...

    async def update_cart(self,user_id: int, item_id: int, update: CartItemUpdate) -> CartItemRead: ...

    async def remove_cart(self, item_id: int, user_id: int) -> CartItemSchema:...

    async def clear_cart_service(self, user_id: int) -> CartItemRead: ...




