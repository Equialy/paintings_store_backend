from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.domain.accounts.schemas.user import UsersSchemaAuth, UsersSchema
from src.domain.pictures.interfaces.pictures import PictureRepositoryProtocol, PictureServiceProtocol
from src.domain.pictures.use_cases.pictures_service import PicturesServiceImpl
from src.infrastructure.database.base import get_async_session
from src.infrastructure.database.repositories.pictures_repo import PicturesRepositoryImpl
from src.presentation.dependencies.authentication.user_dependecies import get_current_auth_user

# --- Repository Dependency ---
SessionAdmin = Annotated[AsyncSession, Depends(get_async_session)]

def get_picture_repository(
    session: SessionAdmin
) -> PictureRepositoryProtocol:
    return PicturesRepositoryImpl(session)

PictureRepository = Annotated[PictureRepositoryProtocol, Depends(get_picture_repository)]

# --- Service Dependency ---

def get_picture_service(
    repo: PictureRepository
) -> PictureServiceProtocol:
    return PicturesServiceImpl(repo)

PictureService = Annotated[PictureServiceProtocol, Depends(get_picture_service)]

# --- Admin Dependency ---

async def get_current_active_user(
    user: UsersSchema = Depends(get_current_auth_user)
) -> UsersSchema:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user

async def get_current_admin_user(
    user: UsersSchema = Depends(get_current_active_user)
) -> UsersSchema:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required"
        )
    return user