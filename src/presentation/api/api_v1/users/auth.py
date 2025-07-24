import logging
from typing import Annotated

import aiohttp
from fastapi import APIRouter, Depends, Form, Response, status, Body
from fastapi.responses import RedirectResponse

import jwt

from src.domain.accounts.schemas.user import TokenJWT, UsersSchemaAdd, UsersSchemaAuth
from src.domain.oauth_google.oauth_google_service import generated_oauth_uri
from src.presentation.dependencies.authentication.user_dependecies import (
    AuthService,
    UserService,
    get_current_auth_user,
)
from src.settings import settings

log = logging.getLogger(__name__)

router = APIRouter(prefix=settings.api.v1.prefix, tags=["JWT"])


@router.post("/login", response_model=TokenJWT)
async def auth_user_jwt(
    auth_service: AuthService,
    username: str = Form(...),
    password: str = Form(...),
) -> TokenJWT:
    username_as_email = username
    user = await auth_service.validate_auth_user(
        email=username_as_email, password=password
    )
    jwt_payload = {"sub": user.email, "username": user.username, "email": user.email}
    token = auth_service.encode_jwt(payload=jwt_payload)
    return TokenJWT(access_token=token, token_type="Bearer")


@router.post("/register", response_model=TokenJWT)
async def register_user(user_in: UsersSchemaAuth, use_case: UserService) -> TokenJWT:
    return await use_case.register_user(user_in)


@router.get("/users/me")
async def auth_current_user(
    user: UsersSchemaAuth = Depends(get_current_auth_user),
) -> dict[str, str]:
    return {"username": user.username, "email": user.email}


@router.get("/google/url")
async def get_google_oath_uri():
    uri = await generated_oauth_uri()
    return RedirectResponse(url=uri, status_code=status.HTTP_302_FOUND)


@router.post("/google/callback")
async def get_google_code(code: Annotated[str, Body(embed=True)]):
    gogle_token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.google_oauth.client_id,
        "client_secret": settings.google_oauth.client_secret,
        "redirect_uri": "http://localhost:3000/auth/google",
        "grant_type": "authorization_code",
        "code": code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=gogle_token_url, data=data, ssl=False) as response:
            result = await response.json()
            id_token = result["id_token"]
            user_data = jwt.decode(
                id_token, algorithms=["RS256"], options={"verify_signature": False}
            )
            bearer_token = result["access_token"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://www.googleapis.com/drive/v3/files",
            headers={"Authorization": f"Bearer {bearer_token}"},
            ssl=False,
        ) as response:
            result = await response.json()
            files = [file["name"] for file in result.get("files", [])]

    return {"user": user_data, "files": files}
