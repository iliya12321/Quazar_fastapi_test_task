from abc import ABC, abstractmethod

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        res = await self.session.execute(
            insert(self.model).values(**data).returning(self.model)
        )
        return res.scalar_one()
