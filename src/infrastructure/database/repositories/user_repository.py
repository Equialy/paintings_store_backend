import logging

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.domain.accounts.schemas.user import UsersSchemaAuth, UsersSchema, UsersSchemaAdd
from src.infrastructure.database.models.users import Users

log = logging.getLogger(__name__)


class UserRepositoryImpl:

    def __init__(self, session: AsyncSession,):
        self.session = session
        self.model = Users

    async def get_by_email(self, email: str) -> UsersSchema | None:
        stmt = sa.select(self.model).where(self.model.email == email).with_for_update()
        result = await self.session.execute(stmt)
        user_obj = result.scalar_one()
        if user_obj is None:
            return None
        return UsersSchema.model_validate(user_obj)

    async def create_user(self, user: UsersSchemaAuth) -> UsersSchema:
        stmt = sa.insert(self.model).values(user.model_dump(exclude_unset=True)).returning(self.model)
        result = await self.session.execute(stmt)
        created = result.scalar_one()
        return UsersSchema.model_validate(created)