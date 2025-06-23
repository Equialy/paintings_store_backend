from datetime import date, datetime
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

class CartItemSchema(BaseModel):
    id: int
    picture_id: int
    quantity: int
    picture: CartItemSchemaRead

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))



class CartItemRead(BaseModel):
    id: int
    user_id: int
    picture_id: int
    quantity: int
    added_at: datetime
    # items: List[CartItemSchema]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))

class CartItemCreate(BaseModel):
    picture_id: int
    quantity: int

class CartItemPaginationResponse(BaseModel):
    items: list[CartItemSchema]

class CartItemUpdate(BaseModel):
    quantity: int
