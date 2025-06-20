import logging

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.domain.pictures.schemas.pictures import PaginationParamsPictures, PictureReadSchema, PictureCreateSchema, \
    PictureUpdateSchema, CategoryRead, CategoryCreate
from src.infrastructure.database.models.pictures import Pictures, Categories
from src.utils.sorted_functions import get_sort_column

logger = logging.getLogger(__name__)

class PicturesRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Pictures

    async def get_all(self, pagination: PaginationParamsPictures) -> list[PictureReadSchema]:
        sort_column = get_sort_column(self.model, pagination.sort_by)
        order_func = sa.desc if pagination.order.lower() == "desc" else sa.asc
        stmt = (
            sa.select(self.model)
            .order_by(order_func(sort_column))
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await self.session.execute(stmt)
        books = result.scalars().all()
        return [PictureReadSchema.model_validate(row) for row in books]

    async def get_by_id(self, picture_id: int) -> PictureReadSchema:
        query = sa.select(self.model).where(self.model.id == picture_id).with_for_update()
        execute = await self.session.execute(query)
        result = execute.scalar_one()

        return PictureReadSchema.model_validate(result)


    async def create(self, schema: PictureCreateSchema) -> PictureReadSchema:
        stmt = sa.insert(self.model).values(schema.model_dump()).returning(self.model)
        model = await self.session.execute(stmt)
        result = model.scalar_one()
        logger.info("Картина %r создана", result.id)
        return PictureReadSchema.model_validate(result)

    async def create_category(self, schema: CategoryCreate) -> CategoryRead:
        stmt = sa.insert(Categories).values(title=schema.title).returning(Categories)
        model = await self.session.execute(stmt)
        result = model.scalar_one()
        logger.info("Создана категория: %s", result)
        return CategoryRead.model_validate(result)

    async def list_category(self) -> list[CategoryRead]:
        stmt = sa.select(Categories)
        model = await self.session.execute(stmt)
        result = model.scalars().all()
        return [CategoryRead.model_validate(obj) for obj in result ]


    async def update(self, picture_id: int, schema: PictureUpdateSchema) -> PictureReadSchema:
        stmt = (sa.update(self.model)
                .where(self.model.id == picture_id)
                .values(schema.model_dump())
                .returning(self.model))
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return PictureReadSchema.model_validate(result)

    async def delete(self, picture_id: int) -> PictureReadSchema:
        stmt = sa.delete(self.model).where(self.model.id == picture_id).returning(self.model)
        execute = await self.session.execute(stmt)
        result = execute.scalar_one()
        return PictureReadSchema.model_validate(result)


