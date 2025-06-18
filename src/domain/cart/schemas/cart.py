from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CartItemSchemaRead(BaseModel):
    id: int
    price: float
    title: str
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))



class CartItemBase(BaseModel):
    picture_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass

class CartItemRead(BaseModel):
    user_id: int
    items: List[CartItemSchemaRead]

class CartItemSchema(CartItemSchemaRead):
    id: int

class CartItemPaginationResponse(BaseModel):
    items: list[CartItemSchema]

class CartItemUpdate(BaseModel):
    quantity: int
