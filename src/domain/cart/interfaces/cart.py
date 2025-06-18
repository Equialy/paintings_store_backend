from typing import Protocol

from src.domain.cart.schemas.cart import CartItemSchema, CartItemPaginationResponse, CartItemRead


class CartRepositoryProtocol(Protocol):

    # async def add(self, book_id: int, reader_id: int) -> CartItemSchema: ...

    async def get_cart(self, user_id: int) ->list[CartItemRead]: ...

    # async def return_borrow(self, book_id: int, borrow_id: int) -> CartItemSchema: ...

class CartServiceProtocol(Protocol):

    # async def add_cart(self, book_id: int, reader_id: int) -> CartItemSchema: ...

    async def get_cart_by_user(self, user_id: int) ->list[CartItemRead]: ...

    # async def return_picture_by_cart(self, book_id: int, borrow_id: int) -> CartItemSchema: ...


