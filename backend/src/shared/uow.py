from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork(Protocol):
    async def commit(self) -> None:...
    async def rollback(self) -> None: ...

class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()