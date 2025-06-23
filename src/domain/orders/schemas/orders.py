from datetime import datetime
from enum import StrEnum
from typing import List
from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel


class OrderItemBase(BaseModel):
    picture_id: int
    quantity: int
    price: float


class OrderItemCreate(BaseModel):
    picture_id: int
    quantity: int
    price: float


class OrderBase(BaseModel):
    address: str
    phone: str

class OrderStatus(StrEnum):
    PENDING   = "Pending"
    PROCESSED = "Processed"
    SHIPPED   = "Shipped"
    DELIVERED = "Delivered"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))


class OrderItemRead(OrderItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))



class OrderRead(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    total: float
    created_at: datetime
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))


class OrderStatusUpdateSchema(BaseModel):
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))

