from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.domain.accounts.services.jwt import JWTService
from src.domain.accounts.services.password_manager import PasswordManagerImpl
from src.infrastructure.database.base import AsyncSessionFactory
from src.infrastructure.database.repositories.user_repository import UserRepositoryImpl
from src.presentation.dependencies.authentication.user_dependecies import (
    Session,
)
from src.settings import settings


class AdminAuth(AuthenticationBackend):

    def __init__(self):
        super().__init__(secret_key=settings.jwt.secret_key)
        #  экземпляры менеджеров
        self._jwt = JWTService()
        self._pwd = PasswordManagerImpl()
        self.session = Session

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        session = AsyncSessionFactory()
        try:
            repo = UserRepositoryImpl(session)
            user = await repo.get_by_email(username)
            if not user or not self._pwd.validate_password(password, user.password):
                return False
            if not user.is_superuser:
                return False

            token = self._jwt.encode_jwt({"sub": user.email, "is_superuser": True})
            request.session.update({"token": token})
            return True

        finally:
            await session.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            payload = self._jwt.decode_jwt(token)
        except Exception:
            return False
        return payload.get("is_superuser", False)


authentication_backend = AdminAuth()
