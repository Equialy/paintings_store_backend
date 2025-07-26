from src.domain.accounts.interfaces.auth import (
    PasswordManagerProtocol,
    JWTServiceProtocol,
)
from src.domain.accounts.interfaces.user import UserRepositoryProtocol
from src.domain.accounts.schemas.user import (
    UsersSchemaAdd,
    TokenJWT,
    UsersSchemaAuth,
    UsersSchema,
)
from src.exceptions.exception_base import NotValidPassword


class UserServiceImpl:
    def __init__(
        self,
        user_repo: UserRepositoryProtocol,
        pwd_manager: PasswordManagerProtocol,
        jwt_manager: JWTServiceProtocol,
    ):
        self.user_repo = user_repo
        self.pwd_mgr = pwd_manager
        self.jwt_mgr = jwt_manager

    async def register_user(self, user_in: UsersSchemaAuth) -> TokenJWT:
        if user_in.password != user_in.password2:
            raise NotValidPassword()
        hashed = self.pwd_mgr.hash_password(user_in.password)
        user_obj = UsersSchemaAdd(
            username=user_in.username,
            email=user_in.email,
            password=hashed,
        )
        saved = await self.user_repo.create_user(user_obj)
        payload = {"sub": saved.email, "email": saved.email}
        token = self.jwt_mgr.encode_jwt(payload)
        return TokenJWT(access_token=token, token_type="Bearer")

    async def get_by_email(self, email: str) -> UsersSchema | None:
        return await self.user_repo.get_by_email(email=email)
