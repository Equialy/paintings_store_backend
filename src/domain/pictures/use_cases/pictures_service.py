import logging

from src.domain.pictures.interfaces.pictures import PictureRepositoryProtocol
from src.domain.pictures.schemas.pictures import (
    PictureReadSchema,
    PictureCreateSchema,
    PictureUpdateSchema,
    PaginationParamsPictures,
    CategoryCreate,
    CategoryRead,
)
from src.exceptions.exception_base import NotFoundError, QuantityError

logger = logging.getLogger(__name__)


class PicturesServiceImpl:

    def __init__(self, books_factory_repository: PictureRepositoryProtocol) -> None:
        self.pictures_factory_repository = books_factory_repository

    async def create_picture(self, schema: PictureCreateSchema) -> PictureReadSchema:
        return await self.pictures_factory_repository.create(schema)

    async def create_category(self, schema: CategoryCreate) -> CategoryRead:
        return await self.pictures_factory_repository.create_category(schema=schema)

    async def get_all_category(self) -> list[CategoryRead]:
        return await self.pictures_factory_repository.list_category()

    async def patch_picture(
        self,
        file_path: str,
        picture_id: int,
    ) -> PictureReadSchema:
        return await self.pictures_factory_repository.patch_picture(
            file_path=file_path, picture_id=picture_id
        )

    async def update_picture(
        self, picture_id: int, schema: PictureUpdateSchema
    ) -> PictureReadSchema:
        return await self.pictures_factory_repository.update(picture_id, schema)

    async def delete_picture(self, picture_id: int) -> None:
        await self.pictures_factory_repository.delete(picture_id)

    async def get_picture(self, picture_id: int) -> PictureReadSchema:
        return await self.pictures_factory_repository.get_by_id(picture_id)

    async def list_pictures(
        self, pagination: PaginationParamsPictures
    ) -> list[PictureReadSchema]:
        return await self.pictures_factory_repository.get_all(pagination)
