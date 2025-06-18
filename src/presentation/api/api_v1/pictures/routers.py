from typing import List

from fastapi import APIRouter, Depends

from src.domain.pictures.schemas.pictures import PictureReadSchema
from src.presentation.dependencies.admin.admin_di import PictureService
from src.presentation.dependencies.pictures.services import PicturesService, PaginationDep
from src.settings import settings

router = APIRouter(prefix=settings.api.v1.prefix, tags=["Pictures Users"])



@router.get("/pictures/{picture_id}", response_model=PictureReadSchema)
async def get_picture_by_id(picture_id: int, picture_service: PicturesService) -> PictureReadSchema:
    return await picture_service.get_picture(picture_id=picture_id)




@router.get("/pictures", response_model=list[PictureReadSchema])
async def list_pictures(
    service: PictureService,
    pagination: PaginationDep
) -> list[PictureReadSchema]:
    return await service.list_pictures(pagination)