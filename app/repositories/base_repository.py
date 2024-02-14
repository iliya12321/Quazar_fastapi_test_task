from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, instance_id: int):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, page: int, size: int) -> list:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, instance_id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, instance_id: int):
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

    async def find_all(self, page: int, size: int) -> list:
        result = await self.session.execute(
            select(self.model)
            .order_by(self.model.id)
            .limit(size)
            .offset((page - 1) * size)
        )
        return result.scalars().all()

    async def find_by_id(self, instance_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.id == instance_id)
        )
        return result.scalar_one_or_none()

    async def update_one(self, instance_id: int, data: dict):
        res = await self.session.execute(
            update(self.model)
            .where(self.model.id == instance_id)
            .values(**data)
            .returning(self.model)
        )
        return res.scalar_one()

    async def delete_by_id(self, instance_id: int):
        await self.session.execute(
            delete(self.model).where(self.model.id == instance_id)
        )
