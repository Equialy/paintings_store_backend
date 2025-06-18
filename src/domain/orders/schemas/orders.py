from datetime import datetime
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


class OrderItemRead(OrderItemBase):
    id: int


    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))


class OrderReadSchema(BaseModel):
    id: int
    user_id: int
    address: str
    phone: str
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemRead]

class OrderBase(BaseModel):
    address: str
    phone: str


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    id: int
    user_id: int
    phone: str
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))

class OrderStatusUpdateSchema(BaseModel):
    status: str = Field(..., description="New status of the order")