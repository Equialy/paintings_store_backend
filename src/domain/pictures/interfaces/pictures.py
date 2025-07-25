from typing import Protocol, List

from src.domain.pictures.schemas.pictures import (
    PictureReadSchema,
    PictureCreateSchema,
    PictureUpdateSchema,
    PaginationParamsPictures,
    CategoryCreate,
    CategoryRead,
)


class PictureRepositoryProtocol(Protocol):
    async def create(self, schema: PictureCreateSchema) -> PictureReadSchema: ...

    async def update(
        self, picture_id: int, schema: PictureUpdateSchema
    ) -> PictureReadSchema: ...

    async def patch_picture(
        self, file_path: str, picture_id: int,
    ) -> PictureReadSchema: ...

    async def delete(self, picture_id: int) -> None: ...

    async def get_by_id(self, picture_id: int) -> PictureReadSchema: ...

    async def get_all(
        self, pagination: PaginationParamsPictures
    ) -> list[PictureReadSchema]: ...

    async def create_category(self, schema: CategoryCreate) -> CategoryRead: ...

    async def list_category(self) -> list[CategoryRead]: ...


class PictureServiceProtocol(Protocol):
    async def create_picture(
        self, schema: PictureCreateSchema
    ) -> PictureReadSchema: ...

    async def create_category(self, schema: CategoryCreate) -> CategoryRead: ...

    async def update_picture(
        self, picture_id: int, schema: PictureUpdateSchema
    ) -> PictureReadSchema: ...

    async def patch_picture(
        self, file_path: str, picture_id: int,
    ) -> PictureReadSchema: ...

    async def delete_picture(self, picture_id: int) -> None: ...

    async def get_picture(self, picture_id: int) -> PictureReadSchema: ...

    async def list_pictures(
        self, pagination: PaginationParamsPictures
    ) -> List[PictureReadSchema]: ...

    async def get_all_category(self) -> list[CategoryRead]: ...
