from typing import Optional

from pydantic import ConfigDict, AliasGenerator, BaseModel, Field
from pydantic.alias_generators import to_camel

class PictureCreateSchema(BaseModel):
    title: str = Field(..., max_length=100)
    author: str = Field(..., max_length=100)
    description: Optional[str]
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    category_id: int

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))


class PictureUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))


class PictureReadSchema(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    price: float
    quantity: int
    category_id: int
    image_url: Optional[str]

    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))





class PaginationParamsPictures(BaseModel):
    limit: int = Field(5, ge=0, le=15, description="Кол-во элементов")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")
    sort_by: str = Field(default="title")
    order: str = Field(default="desc")
