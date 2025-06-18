import logging

from src.domain.pictures.interfaces.pictures import PictureRepositoryProtocol
from src.domain.pictures.schemas.pictures import PictureReadSchema, PictureCreateSchema, PictureUpdateSchema, \
    PaginationParamsPictures
from src.exceptions.exception_base import NotFoundError, QuantityError

logger = logging.getLogger(__name__)


class PicturesServiceImpl:

    def __init__(self, books_factory_repository: PictureRepositoryProtocol) -> None:
        self.pictures_factory_repository = books_factory_repository

    async def create_picture(self, schema: PictureCreateSchema) -> PictureReadSchema:
        return await self.pictures_factory_repository.create(schema)

    async def update_picture(self, picture_id: int, schema: PictureUpdateSchema) -> PictureReadSchema:
        return await self.pictures_factory_repository.update(picture_id, schema)

    async def delete_picture(self, picture_id: int) -> None:
        await self.pictures_factory_repository.delete(picture_id)

    async def get_picture(self, picture_id: int) -> PictureReadSchema:
        return await self.pictures_factory_repository.get_by_id(picture_id)

    async def list_pictures(self,pagination: PaginationParamsPictures ) -> list[PictureReadSchema]:
        return await self.pictures_factory_repository.get_all(pagination)