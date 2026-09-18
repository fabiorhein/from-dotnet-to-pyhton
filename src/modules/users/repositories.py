import uuid
from typing import Protocol

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class IUserRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None: ...
    async def get_by_id(self, id: uuid.UUID) -> User | None: ...
    async def get_all(self) -> list[User]: ...
    async def get_all_without_inactive(self) -> list[User]: ...
    async def add(self, user: User) -> None: ...
    async def update(self, user: User) -> User: ...


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        query = sqlalchemy.select(User).where(User.email == email)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, id: uuid.UUID) -> User | None:
        return await self._session.get(User, id)

    async def get_all(self) -> list[User]:
        query = sqlalchemy.select(User)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_all_without_inactive(self) -> list[User]:
        query = sqlalchemy.select(User).where(User.is_active == True)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def add(self, user: User) -> None:
        self._session.add(user)
        await self._session.flush()

    async def update(self, user: User) -> User:
        await self._session.flush()
        return user