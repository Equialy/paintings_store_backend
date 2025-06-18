from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.pictures.interfaces.pictures import PictureRepositoryProtocol, PictureServiceProtocol
from src.domain.pictures.schemas.pictures import PaginationParamsPictures
from src.domain.pictures.use_cases.pictures_service import PicturesServiceImpl
from src.infrastructure.database.base import get_async_session
from src.infrastructure.database.repositories.pictures_repo import PicturesRepositoryImpl

# --- repositories ---

Session = Annotated[AsyncSession, Depends(get_async_session)]

def get_pictures_repositories(session: Session) -> PictureRepositoryProtocol:
    return PicturesRepositoryImpl(session)

PicturesFactoryRepository = Annotated[PictureRepositoryProtocol, Depends(get_pictures_repositories)]

# --- services ---

def get_pictures_service(pictures_factory_repositories: PicturesFactoryRepository) -> PictureServiceProtocol:
    return PicturesServiceImpl(pictures_factory_repositories)


PicturesService = Annotated[PictureServiceProtocol, Depends(get_pictures_service)]

PaginationDep = Annotated[PaginationParamsPictures,Depends(PaginationParamsPictures)]