from sqladmin import ModelView

from src.infrastructure.database.models.cart_item import CartItem
from src.infrastructure.database.models.orders import Order, OrderItem
from src.infrastructure.database.models.pictures import Pictures, Categories
from src.infrastructure.database.models.users import Users


class UserAdmin(ModelView, model=Users):
    column_list = [
        Users.id,
        Users.username,
        Users.email,
        Users.is_superuser,
        Users.orders,
        Users.created_at,
    ]
    can_delete = False
    column_details_exclude_list = [Users.password]
    form_edit_excluded_columns = ["password"]
    form_ajax_refs = {
        "cart_items": {"fields": ["id", "picture_id"]},
        "orders": {"fields": ["id"]},
    }


class PictureAdmin(ModelView, model=Pictures):
    column_list = [
        Pictures.title,
        Pictures.description,
        Pictures.category,
        Pictures.author,
        Pictures.price,
        Pictures.category_id,
        Pictures.quantity,
        Pictures.created_at,
    ]
    name = "Картина"
    name_plural = "Картины"


class CategoryAdmin(ModelView, model=Categories):
    column_list = [
        Categories.id,
        Categories.title,
        Categories.pictures,
    ]
    name = "Категория"
    name_plural = "Категории"


class OrdersAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.address,
        Order.phone,
        Order.status,
        Order.total,
        Order.created_at,
    ]
    name = "Заказ"
    name_plural = "Заказы"

    form_ajax_refs = {"items": {"fields": ["id", "picture_id"]}}


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [
        CartItem.id,
        CartItem.user_id,
        CartItem.picture_id,
        CartItem.quantity,
        CartItem.added_at,
    ]
    name = "Предмет корзины"
    name_plural = "Предметы корзины"


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [
        OrderItem.id,
        OrderItem.order_id,
        OrderItem.picture_id,
        OrderItem.quantity,
        OrderItem.price,
    ]

    name = "Предмет заказа"
    name_plural = "Предметы заказа"
