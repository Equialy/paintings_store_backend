from src.domain.cart.interfaces.cart import CartRepositoryProtocol
from src.domain.cart.schemas.cart import CartItemPaginationResponse, CartItemSchema, CartItemRead


class CartServiceImpl:
    def __init__(self, cart_factory_repository: CartRepositoryProtocol):
        self.cart_factory_repository = cart_factory_repository

    async def get_cart_by_user(self, user_id: int) -> list[CartItemRead]:
        return await self.cart_factory_repository.get_cart(user_id=user_id)
    #
    # async def add_borrow(self, book_id: int, reader_id: int) -> CartItemSchema:
    #     return await self.cart_factory_repository.add(book_id=book_id, reader_id=reader_id)
    #
    # async def return_book_by_borrow(self, book_id: int, borrow_id: int) -> CartItemSchema:
    #     return await self.cart_factory_repository.return_borrow(book_id=book_id, borrow_id=borrow_id)
